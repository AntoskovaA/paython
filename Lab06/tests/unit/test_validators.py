import pytest
from reliable_finance.validators import parse_transaction
from reliable_finance.exceptions import RecordValidationError


@pytest.mark.parametrize(
    "amount_str, expected",
    [
        ("100.0", 100.0),
        ("5000", 5000.0),
    ]
)
def test_valid_amounts(amount_str, expected):
    row = {"date": "2026-10-01", "category": "Продукти", "amount": amount_str, "type": "expense", "description": "хліб"}
    record = parse_transaction(row, line_number=2, allowed_categories=("Продукти",))
    assert record.amount == pytest.approx(expected)


def test_invalid_amount_raises_error():
    row = {"date": "2026-10-01", "category": "Продукти", "amount": "-50", "type": "expense", "description": ""}
    with pytest.raises(RecordValidationError) as exc_info:
        parse_transaction(row, line_number=3, allowed_categories=("Продукти",))
    assert exc_info.value.field == "amount"


def test_disallowed_category_raises_error():
    row = {"date": "2026-10-01", "category": "Заборонена", "amount": "200", "type": "expense", "description": ""}
    with pytest.raises(RecordValidationError, match="не входить до переліку"):
        parse_transaction(row, line_number=4, allowed_categories=("Продукти",))