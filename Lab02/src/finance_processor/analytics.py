from collections.abc import Callable
from typing import Any
from finance_processor.decorators import measure_time


@measure_time
def calculate_balance(items: list[dict]) -> float:
    """Агрегація балансу з використанням генераторних виразів."""
    income = sum(item["amount"] for item in items if item["type"] == "income")
    expense = sum(item["amount"] for item in items if item["type"] == "expense")
    return income - expense


def calculate_category_expenses(items: list[dict]) -> dict[str, float]:
    """Підрахунок витрат для кожної категорії окремо."""
    expenses: dict[str, float] = {}
    for item in items:
        if item["type"] == "expense":
            cat = item["category"]
            expenses[cat] = expenses.get(cat, 0.0) + item["amount"]
    return expenses


def find_largest_expense(items: list[dict]) -> dict | None:
    """Пошук найбільшої витрати через вбудовану функцію max та lambda."""
    expense_items = [i for i in items if i["type"] == "expense"]
    if not expense_items:
        return None
    return max(expense_items, key=lambda x: x["amount"])


def create_amount_filter(min_amount: float) -> Callable[[dict], bool]:
    """Closure (замикання): повертає функцію-фільтр, що пам'ятає min_amount."""
    def predicate(item: dict) -> bool:
        return item["amount"] >= min_amount

    return predicate


def calculate_sum_of_adjustments(*amounts: float) -> float:
    """Демонстрація *args: обчислення суми змінної кількості коригувань."""
    return sum(amounts)


def create_transaction_record(**fields: Any) -> dict:
    """Демонстрація **kwargs: створення словника операції з довільних ключів."""
    return dict(fields)