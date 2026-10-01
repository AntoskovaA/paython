from abc import ABC, abstractmethod
from dataclasses import dataclass
from finance_domain.value_objects import Money


@dataclass(frozen=True)
class Category:
    name: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Назва категорії не може бути порожньою!")


class Transaction(ABC):
    """Базовий клас транзакції з інкапсуляцією та property."""

    def __init__(self, id_: int, date_: str, category: Category, money: Money, description: str) -> None:
        self.id = id_
        self._date = date_
        self._category = category
        self._money = money
        self._description = description

    @property
    def money(self) -> Money:
        return self._money

    @property
    def category(self) -> Category:
        return self._category

    @property
    def date(self) -> str:
        return self._date

    @property
    def description(self) -> str:
        return self._description

    @abstractmethod
    def get_signed_amount(self) -> float:
        """Повертає значення з урахуванням знаку операції."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, money={self._money}, cat='{self._category.name}')"


class Income(Transaction):
    """Клас доходів (успадкування від Transaction)."""

    def __init__(self, id_: int, date_: str, category: Category, money: Money, description: str = "") -> None:
        super().__init__(id_, date_, category, money, description)

    def get_signed_amount(self) -> float:
        return self._money.amount


class Expense(Transaction):
    """Клас витрат (успадкування від Transaction)."""

    def __init__(self, id_: int, date_: str, category: Category, money: Money, description: str = "") -> None:
        super().__init__(id_, date_, category, money, description)

    def get_signed_amount(self) -> float:
        return -self._money.amount


class FinancialTracker:
    """Контейнерний клас: використовує композицію для агрегації списку транзакцій."""

    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    def add(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def __len__(self) -> int:
        return len(self._transactions)

    def __iter__(self):
        return iter(self._transactions)

    def __contains__(self, transaction_id: int) -> bool:
        return any(t.id == transaction_id for t in self._transactions)

    @property
    def transactions(self) -> list[Transaction]:
        return list(self._transactions)