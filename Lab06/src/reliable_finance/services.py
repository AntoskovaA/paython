from collections.abc import Iterable, Iterator
from dataclasses import dataclass
import logging
from pathlib import Path
from reliable_finance.exceptions import RecordValidationError
from reliable_finance.models import TransactionRecord
from reliable_finance.readers import read_csv_rows
from reliable_finance.validators import parse_transaction

logger = logging.getLogger("reliable_finance.service")


@dataclass
class ImportStatistics:
    total: int = 0
    valid: int = 0
    invalid: int = 0


def import_transactions(
    path: Path,
    *,
    skip_invalid: bool,
    allowed_categories: tuple[str, ...],
    statistics: ImportStatistics,
) -> Iterator[TransactionRecord]:
    """Потоковий імпорт операцій із політикою обробки помилок strict або tolerant."""
    for line_number, row in read_csv_rows(path):
        statistics.total += 1
        try:
            record = parse_transaction(
                row,
                line_number=line_number,
                allowed_categories=allowed_categories,
            )
        except RecordValidationError as error:
            statistics.invalid += 1
            logger.warning(
                "Некоректний запис у рядку %s (поле '%s'): %s",
                error.line_number,
                error.field,
                error,
            )
            if skip_invalid:
                continue
            raise
        statistics.valid += 1
        yield record


def filter_by_minimum_amount(
    records: Iterable[TransactionRecord], minimum_amount: float
) -> Iterator[TransactionRecord]:
    """Фільтрація валідного потоку за пороговою сумою."""
    for record in records:
        if record.amount >= minimum_amount:
            yield record