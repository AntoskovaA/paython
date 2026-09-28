from collections.abc import Iterable, Iterator
from finance_stream.models import TransactionRecord


def validate_transactions(rows: Iterable[dict[str, str]]) -> Iterator[TransactionRecord]:
    """Валідація значень та створення типізованих записів."""
    for row in rows:
        try:
            date_val = row["date"].strip()
            category = row["category"].strip()
            amount = float(row["amount"])
            op_type = row["type"].strip().lower()
            description = row.get("description", "").strip()
        except (ValueError, KeyError, TypeError):
            continue

        if not date_val or not category or amount <= 0:
            continue
        if op_type not in ("income", "expense"):
            continue

        yield TransactionRecord(
            date=date_val,
            category=category,
            amount=amount,
            op_type=op_type,
            description=description,
        )


def filter_by_type(records: Iterable[TransactionRecord], op_type: str) -> Iterator[TransactionRecord]:
    """Фільтрація за типом операції."""
    for record in records:
        if record.op_type == op_type:
            yield record


def filter_expenses_by_threshold(
    records: Iterable[TransactionRecord], category: str, threshold: float
) -> Iterator[TransactionRecord]:
    """Фільтрація витрат за категорією та мінімальною сумою."""
    for record in records:
        if record.op_type == "expense" and record.category == category and record.amount >= threshold:
            yield record