from pathlib import Path
import json
import pytest
from reliable_finance.services import ImportStatistics, filter_by_minimum_amount, import_transactions
from reliable_finance.exporters import atomic_export_json


@pytest.mark.integration
def test_full_pipeline_integration(sample_config):
    stats = ImportStatistics()
    stream = import_transactions(
        sample_config.input_path,
        skip_invalid=sample_config.processing.skip_invalid,
        allowed_categories=sample_config.processing.allowed_categories,
        statistics=stats
    )
    filtered = filter_by_minimum_amount(stream, sample_config.processing.minimum_amount)
    count = atomic_export_json(filtered, sample_config.output_path)
    assert count == 1
    assert sample_config.output_path.exists()
    data = json.loads(sample_config.output_path.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["category"] == "Зарплата"


@pytest.mark.integration
def test_pipeline_tolerant_mode(tmp_path: Path):
    csv_file = tmp_path / "trans.csv"
    csv_file.write_text(
        "date,category,amount,type,description\n"
        "2026-10-01,Зарплата,5000.0,income,робота\n"
        "2026-10-02,,помилкова_сума,expense,битий рядок\n"
        "2026-10-03,Продукти,300.0,expense,їжа\n",
        encoding="utf-8"
    )
    out_json = tmp_path / "out.json"
    stats = ImportStatistics()
    stream = import_transactions(
        csv_file,
        skip_invalid=True,
        allowed_categories=("Зарплата", "Продукти"),
        statistics=stats
    )
    count = atomic_export_json(stream, out_json)
    assert stats.total == 3
    assert stats.valid == 2
    assert stats.invalid == 1
    assert count == 2


@pytest.mark.integration
def test_pipeline_empty_result(tmp_path: Path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("date,category,amount,type,description\n", encoding="utf-8")
    out_json = tmp_path / "empty.json"
    stats = ImportStatistics()
    stream = import_transactions(
        csv_file,
        skip_invalid=True,
        allowed_categories=("Зарплата",),
        statistics=stats
    )
    count = atomic_export_json(stream, out_json)
    assert count == 0
    assert out_json.exists()
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data == []