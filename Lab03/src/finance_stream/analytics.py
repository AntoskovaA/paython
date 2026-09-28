from collections import Counter
from collections.abc import Iterable, Iterator
from itertools import accumulate
from finance_stream.models import TransactionRecord


def stream_financial_summary(records: Iterable[TransactionRecord]) -> dict:
    """Агрегація балансу та витрат за один прохід по потоку."""
    total_income = 0.0
    total_expense = 0.0
    category_expenses: Counter = Counter()

    for r in records:
        if r.op_type == "income":
            total_income += r.amount
        elif r.op_type == "expense":
            total_expense += r.amount
            category_expenses[r.category] += r.amount

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "category_expenses": dict(category_expenses),
    }


def stream_cumulative_balance(records: Iterable[TransactionRecord]) -> Iterator[float]:
    """Обчислення кумулятивного балансу за допомогою itertools.accumulate."""
    signed_amounts = (
        r.amount if r.op_type == "income" else -r.amount for r in records
    )
    yield from accumulate(signed_amounts)