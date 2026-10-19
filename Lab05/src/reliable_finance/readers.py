import csv
from collections.abc import Iterator
from pathlib import Path
from reliable_finance.exceptions import DataImportError


def read_csv_rows(path: Path) -> Iterator[tuple[int, dict[str, str]]]:
    """Потокове читання рядків CSV із передачею номера рядка для звітності."""
    try:
        with path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for line_number, row in enumerate(reader, start=2):
                yield line_number, row
    except OSError as error:
        raise DataImportError(f"Неможливо прочитати вхідний файл: {path}") from error