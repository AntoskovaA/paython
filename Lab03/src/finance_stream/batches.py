from collections.abc import Iterable, Iterator
from itertools import islice
from finance_stream.models import TransactionRecord


def batched_transactions(
    records: Iterable[TransactionRecord], batch_size: int
) -> Iterator[list[TransactionRecord]]:
    """Розбиття потоку на порції (батчі) за допомогою itertools.islice."""
    iterator = iter(records)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            return
        yield batch