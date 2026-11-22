from pathlib import Path
import pytest
from sqlalchemy.orm import Session

from reliable_finance.db_api_queries import summarize_operations_by_category_and_period
from reliable_finance.db_models import Category, FinancialOperation
from reliable_finance.repositories import (
    CategoryRepository,
    FinancialOperationRepository,
    batch_import_operations,
)


@pytest.mark.integration
def test_crud_categories_and_operations(db_session: Session) -> None:
    cat_repo = CategoryRepository(db_session)
    op_repo = FinancialOperationRepository(db_session)

    # Create
    food = cat_repo.add("Продукти", "expense")
    salary = cat_repo.add("Зарплата", "income")
    assert food.id is not None
    assert salary.id is not None

    op = op_repo.add(
        date="2026-10-05",
        amount=450.0,
        op_type="expense",
        category_id=food.id,
    )
    assert op.id is not None

    # Read
    loaded = op_repo.get_by_id(op.id)
    assert loaded is not None
    assert loaded.amount == 450.0

    # Update
    updated = op_repo.update_amount(op.id, 500.0)
    assert updated is not None
    assert updated.amount == 500.0

    # Delete
    assert op_repo.delete(op.id) is True
    assert op_repo.get_by_id(op.id) is None


@pytest.mark.integration
def test_totals_balance_category_aggregation_and_filters(db_session: Session) -> None:
    cat_repo = CategoryRepository(db_session)
    op_repo = FinancialOperationRepository(db_session)

    salary = cat_repo.add("Зарплата", "income")
    food = cat_repo.add("Продукти", "expense")
    transport = cat_repo.add("Транспорт", "expense")

    op_repo.add("2026-10-01", 20000.0, "income", salary.id)
    op_repo.add("2026-10-03", 1200.0, "expense", food.id)
    op_repo.add("2026-10-15", 600.0, "expense", transport.id)
    op_repo.add("2026-11-02", 800.0, "expense", food.id)

    assert op_repo.total_by_type("income") == pytest.approx(20000.0)
    assert op_repo.total_by_type("expense") == pytest.approx(2600.0)
    assert op_repo.get_balance() == pytest.approx(17400.0)

    by_cat = dict(op_repo.expenses_by_category())
    assert by_cat["Продукти"] == pytest.approx(2000.0)
    assert by_cat["Транспорт"] == pytest.approx(600.0)

    oct_ops = op_repo.filter_by_date_range("2026-10-01", "2026-10-31")
    assert len(oct_ops) == 3

    monthly = op_repo.monthly_statistics()
    assert ("2026-10", 20000.0, 1800.0) in monthly
    assert ("2026-11", 0.0, 800.0) in monthly


@pytest.mark.integration
def test_batch_import_rollback_on_invalid_record(db_session: Session) -> None:
    cat_repo = CategoryRepository(db_session)
    op_repo = FinancialOperationRepository(db_session)
    food = cat_repo.add("Продукти", "expense")

    items = [
        {"date": "2026-10-10", "amount": 300.0, "op_type": "expense", "category_id": food.id},
        {"date": "2026-10-11", "amount": -50.0, "op_type": "expense", "category_id": food.id},
    ]

    with pytest.raises(ValueError):
        batch_import_operations(db_session, items)

    # Через rollback жоден запис із пакета не повинен залишитися у БД
    assert op_repo.get_all() == []


@pytest.mark.integration
def test_db_api_parameterized_summary(sqlite_db_file: Path) -> None:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(f"sqlite:///{sqlite_db_file}", echo=False)
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        cat_repo = CategoryRepository(session)
        op_repo = FinancialOperationRepository(session)
        food = cat_repo.add("Продукти", "expense")
        op_repo.add("2026-10-05", 400.0, "expense", food.id)
        op_repo.add("2026-10-20", 600.0, "expense", food.id)
        op_repo.add("2026-12-01", 999.0, "expense", food.id)

    result = summarize_operations_by_category_and_period(
        database_path=sqlite_db_file,
        op_type="expense",
        start_date="2026-10-01",
        end_date="2026-10-31",
    )
    assert result == [("Продукти", 1000.0, 2)]