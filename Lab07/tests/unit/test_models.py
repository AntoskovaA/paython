from reliable_finance.models import TransactionRecord, ProcessingConfig, LoggingConfig


def test_transaction_record_to_dict():
    record = TransactionRecord(
        date="2026-10-01",
        category="Зарплата",
        amount=10000.0,
        op_type="income",
        description="Аванс"
    )
    d = record.to_dict()
    assert d["amount"] == 10000.0
    assert d["category"] == "Зарплата"
    assert d["op_type"] == "income"


def test_processing_config_properties():
    pc = ProcessingConfig(minimum_amount=50.0, skip_invalid=False, allowed_categories=("А",))
    assert pc.minimum_amount == 50.0
    assert pc.skip_invalid is False


def test_logging_config_properties(tmp_path):
    lc = LoggingConfig(level="DEBUG", path=tmp_path / "log.txt")
    assert lc.level == "DEBUG"