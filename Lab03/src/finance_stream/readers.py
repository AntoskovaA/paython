from collections.abc import Iterator
from pathlib import Path


def read_lines(file_path: Path) -> Iterator[str]:
    """Потокове читання файлу рядок за рядком через yield from."""
    with file_path.open("r", encoding="utf-8") as file:
        yield from file