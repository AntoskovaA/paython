from __future__ import annotations

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from reliable_finance.db_models import Category, FinancialOperation


class CategoryRepository:
    """Репозиторій для роботи з категоріями фінансових операцій."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str, op_type: str) -> Category:
        category = Category(name=name, op_type=op_type)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def get_by_id(self, category_id: int) -> Category | None:
        return self.session.get(Category, category_id)

    def get_by_name(self, name: str) -> Category | None:
        statement = select(Category).where(Category.name == name)
        return self.session.scalar(statement)

    def get_all(self) -> list[Category]:
        statement = select(Category)
        return list(self.session.scalars(statement))

    def update_name(self, category_id: int, new_name: str) -> Category | None:
        category = self.get_by_id(category_id)
        if category is None:
            return None
        category.name = new_name
        self.session.commit()
        self.session.refresh(category)
        return category

    def delete(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if category is None:
            return False
        self.session.delete(category)
        self.session.commit()
        return True


class FinancialOperationRepository:
    """Репозиторій для CRUD, фільтрації та аналітики фінансових операцій."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(
        self,
        date: str,
        amount: float,
        op_type: str,
        category_id: int,
    ) -> FinancialOperation:
        operation = FinancialOperation(
            date=date,
            amount=amount,
            op_type=op_type,
            category_id=category_id,
        )
        self.session.add(operation)
        self.session.commit()
        self.session.refresh(operation)
        return operation

    def get_by_id(self, operation_id: int) -> FinancialOperation | None:
        return self.session.get(FinancialOperation, operation_id)

    def get_all(self) -> list[FinancialOperation]:
        statement = select(FinancialOperation)
        return list(self.session.scalars(statement))

    def filter_by_date_range(self, start_date: str, end_date: str) -> list[FinancialOperation]:
        statement = (
            select(FinancialOperation)
            .where(FinancialOperation.date >= start_date, FinancialOperation.date <= end_date)
            .order_by(FinancialOperation.date)
        )
        return list(self.session.scalars(statement))

    def filter_by_category(self, category_id: int) -> list[FinancialOperation]:
        statement = select(FinancialOperation).where(FinancialOperation.category_id == category_id)
        return list(self.session.scalars(statement))

    def update_amount(self, operation_id: int, new_amount: float) -> FinancialOperation | None:
        operation = self.get_by_id(operation_id)
        if operation is None:
            return None
        operation.amount = new_amount
        self.session.commit()
        self.session.refresh(operation)
        return operation

    def delete(self, operation_id: int) -> bool:
        operation = self.get_by_id(operation_id)
        if operation is None:
            return False
        self.session.delete(operation)
        self.session.commit()
        return True

    def total_by_type(self, op_type: str) -> float:
        statement = select(func.sum(FinancialOperation.amount)).where(
            FinancialOperation.op_type == op_type
        )
        result = self.session.scalar(statement)
        return float(result) if result is not None else 0.0

    def get_balance(self) -> float:
        return self.total_by_type("income") - self.total_by_type("expense")

    def expenses_by_category(self) -> list[tuple[str, float]]:
        statement = (
            select(Category.name, func.sum(FinancialOperation.amount))
            .join(FinancialOperation, FinancialOperation.category_id == Category.id)
            .where(FinancialOperation.op_type == "expense")
            .group_by(Category.name)
        )
        rows = self.session.execute(statement).all()
        return [(name, float(total or 0.0)) for name, total in rows]

    def monthly_statistics(self) -> list[tuple[str, float, float]]:
        """Повертає список кортежів (рік-місяць 'YYYY-MM', сума доходів, сума витрат)."""
        month_expr = func.substr(FinancialOperation.date, 1, 7)
        income_sum = func.sum(
            case((FinancialOperation.op_type == "income", FinancialOperation.amount), else_=0.0)
        )
        expense_sum = func.sum(
            case((FinancialOperation.op_type == "expense", FinancialOperation.amount), else_=0.0)
        )
        statement = (
            select(month_expr, income_sum, expense_sum)
            .group_by(month_expr)
            .order_by(month_expr)
        )
        rows = self.session.execute(statement).all()
        return [
            (str(month), float(inc or 0.0), float(exp or 0.0))
            for month, inc, exp in rows
        ]


def batch_import_operations(
    session: Session,
    items: list[dict[str, object]],
) -> list[FinancialOperation]:
    """
    Пакетний імпорт операцій в одній транзакції.
    Якщо хоча б один запис некоректний — виконується rollback(), зміни не зберігаються.
    """
    created: list[FinancialOperation] = []
    try:
        for item in items:
            amount = float(item["amount"])  # type: ignore[arg-type]
            op_type = str(item["op_type"])
            date = str(item["date"])
            category_id = int(item["category_id"])  # type: ignore[arg-type]

            if amount <= 0:
                raise ValueError(f"Сума операції має бути додатною, отримано: {amount}")
            if op_type not in {"income", "expense"}:
                raise ValueError(f"Некоректний тип операції: {op_type}")

            category = session.get(Category, category_id)
            if category is None:
                raise ValueError(f"Категорію з id={category_id} не знайдено")

            op = FinancialOperation(
                date=date,
                amount=amount,
                op_type=op_type,
                category_id=category_id,
            )
            session.add(op)
            created.append(op)

        session.commit()
        for op in created:
            session.refresh(op)
        return created
    except Exception:
        session.rollback()
        raise