from collections.abc import Iterator
from pathlib import Path
from finance_stream.filters import validate_transactions
from finance_stream.models import TransactionRecord
from finance_stream.parsers import parse_csv_rows
from finance_stream.readers import read_lines
from finance_stream.transformations import normalize_transactions


def build_finance_pipeline(file_path: Path) -> Iterator[TransactionRecord]:
    """Збирання повного лінивого конвеєра обробки."""
    lines = read_lines(file_path)
    rows = parse_csv_rows(lines)
    valid_records = validate_transactions(rows)
    normalized = normalize_transactions(valid_records)
    return normalized