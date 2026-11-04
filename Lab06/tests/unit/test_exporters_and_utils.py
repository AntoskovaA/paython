from pathlib import Path
import pytest
from reliable_finance.models import TransactionRecord
from reliable_finance.exporters import atomic_export_json
from reliable_finance.utils import logged_operation
from reliable_finance.exceptions import DataExportError


def test_atomic_export_success(tmp_path: Path):
    out = tmp_path / "result.json"
    records = [
        TransactionRecord(
            date="2026-10-01",
            category="Зарплата",
            amount=1000.0,
            op_type="income",
            description="тест"
        )
    ]
    count = atomic_export_json(records, out)
    assert count == 1
    assert out.exists()


def test_logged_operation_context():
    with logged_operation("Тестова операція"):
        x = 1 + 1
    assert x == 2