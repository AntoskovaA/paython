import csv
from collections.abc import Iterable, Iterator


def parse_csv_rows(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    """Потоковий розбір рядків за допомогою DictReader без завантаження в пам'ять."""
    reader = csv.DictReader(lines)
    yield from reader