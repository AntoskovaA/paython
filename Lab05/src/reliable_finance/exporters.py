from collections.abc import Iterable
import json
from pathlib import Path
from reliable_finance.exceptions import DataExportError
from reliable_finance.models import TransactionRecord


def atomic_export_json(records: Iterable[TransactionRecord], path: Path) -> int:
    """Атомарний потоковий експорт у JSON через тимчасовий файл."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    count = 0

    try:
        with temp_path.open("w", encoding="utf-8") as file:
            file.write("[\n")
            first = True
            for record in records:
                if not first:
                    file.write(",\n")
                json.dump(record.to_dict(), file, ensure_ascii=False, indent=2)
                first = False
                count += 1
            file.write("\n]\n")

        # Атомарне заміщення цільового файлу
        temp_path.replace(path)
    except (OSError, TypeError) as error:
        temp_path.unlink(missing_ok=True)
        raise DataExportError(f"Збій експорту у файл {path}: операцію скасовано") from error

    return count