from collections.abc import Iterable, Iterator
from finance_stream.models import TransactionRecord


def normalize_transactions(records: Iterable[TransactionRecord]) -> Iterator[TransactionRecord]:
    """Нормалізація регістру категорій та описів у потоці."""
    for record in records:
        yield record._replace(
            category=record.category.strip().title(),
            description=record.description.strip().capitalize(),
        )