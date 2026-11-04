from pathlib import Path
import pytest
from unittest.mock import Mock
from reliable_finance.services import ImportStatistics, import_transactions, filter_by_minimum_amount
from reliable_finance.config import load_config
from reliable_finance.exceptions import ConfigurationError


def test_import_transactions_with_tmp_path(tmp_path: Path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "date,category,amount,type,description\n"
        "2026-10-01,Продукти,500.0,expense,магазин\n"
        "2026-10-02,,помилка,expense,порожньо\n",
        encoding="utf-8"
    )
    stats = ImportStatistics()
    records = list(import_transactions(
        csv_file,
        skip_invalid=True,
        allowed_categories=("Продукти",),
        statistics=stats
    ))
    assert stats.total == 2
    assert stats.valid == 1
    assert stats.invalid == 1
    assert len(records) == 1
    assert records[0].amount == 500.0


def test_filter_minimum_amount(sample_records):
    filtered = list(filter_by_minimum_amount(sample_records, 1000.0))
    assert len(filtered) == 1
    assert filtered[0].amount == 12000.0


def test_load_config_fail_fast(monkeypatch, tmp_path: Path):
    bad_yaml = tmp_path / "bad_config.yaml"
    bad_yaml.write_text("invalid_structure: true", encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_config(bad_yaml)


def test_mock_return_value_and_interaction(mock_notifier):
    # Перевірка Mock, return_value та interaction assertion
    mock_notifier.send("test@example.com", "Hello")
    mock_notifier.send.assert_called_once_with("test@example.com", "Hello")


def test_mock_side_effect():
    # Перевірка side_effect у Mock
    mock_gateway = Mock()
    mock_gateway.pay.side_effect = ValueError("Network error")
    with pytest.raises(ValueError, match="Network error"):
        mock_gateway.pay(100)