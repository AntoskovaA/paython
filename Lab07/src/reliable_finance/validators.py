from reliable_finance.exceptions import RecordValidationError
from reliable_finance.models import TransactionRecord


def parse_transaction(
    row: dict[str, str],
    *,
    line_number: int,
    allowed_categories: tuple[str, ...],
) -> TransactionRecord:
    """Парсинг та валідація рядка з ланцюжком винятків (exception chaining)."""
    date_val = row.get("date", "").strip()
    if not date_val:
        raise RecordValidationError("Порожня дата операції", line_number=line_number, field="date")

    category = row.get("category", "").strip()
    if not category:
        raise RecordValidationError("Категорія не вказана", line_number=line_number, field="category")

    if category not in allowed_categories:
        raise RecordValidationError(
            f"Категорія '{category}' не входить до переліку дозволених у конфігурації",
            line_number=line_number,
            field="category",
        )

    try:
        amount = float(row.get("amount", ""))
    except (ValueError, TypeError) as error:
        raise RecordValidationError(
            "Сума транзакції повинна бути дійсним числом",
            line_number=line_number,
            field="amount",
        ) from error

    if amount <= 0:
        raise RecordValidationError(
            f"Сума має бути строго більшою за 0 (отримано {amount})",
            line_number=line_number,
            field="amount",
        )

    op_type = row.get("type", "").strip().lower()
    if op_type not in ("income", "expense"):
        raise RecordValidationError(
            f"Некоректний тип операції: '{op_type}'. Очікується income або expense",
            line_number=line_number,
            field="type",
        )

    description = row.get("description", "").strip()

    return TransactionRecord(
        date=date_val,
        category=category,
        amount=amount,
        op_type=op_type,
        description=description,
    )