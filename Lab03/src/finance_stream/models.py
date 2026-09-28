from typing import NamedTuple


class TransactionRecord(NamedTuple):
    date: str
    category: str
    amount: float
    op_type: str  # "income" або "expense"
    description: str


class TransactionLimitIterator:
    """Власний клас-ітератор з протоколом __iter__ та __next__."""

    def __init__(self, transactions: list[TransactionRecord], max_count: int) -> None:
        self._data = transactions
        self._limit = min(max_count, len(transactions))
        self._index = 0

    def __iter__(self) -> "TransactionLimitIterator":
        return self

    def __next__(self) -> TransactionRecord:
        if self._index >= self._limit:
            raise StopIteration
        record = self._data[self._index]
        self._index += 1
        return record