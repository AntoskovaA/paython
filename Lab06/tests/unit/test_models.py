from reliable_finance.models import TransactionRecord


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