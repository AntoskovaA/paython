from pathlib import Path
import pytest
from unittest.mock import Mock
from reliable_finance.models import ProcessingConfig, LoggingConfig, AppConfig, TransactionRecord


@pytest.fixture
def sample_config(tmp_path: Path) -> AppConfig:
    """Фікстура №1: тестова конфігурація."""
    input_file = tmp_path / "test_input.csv"
    input_file.write_text("date,category,amount,type,description\n2026-10-01,Зарплата,15000.0,income,Тест", encoding="utf-8")
    
    output_file = tmp_path / "output.json"
    log_file = tmp_path / "app.log"

    return AppConfig(
        input_path=input_file,
        output_path=output_file,
        processing=ProcessingConfig(
            minimum_amount=100.0,
            skip_invalid=True,
            allowed_categories=("Зарплата", "Продукти", "Транспорт"),
        ),
        logging=LoggingConfig(level="INFO", path=log_file),
    )


@pytest.fixture
def sample_records() -> list[TransactionRecord]:
    """Фікстура №2: список тестових транзакцій."""
    return [
        TransactionRecord(date="2026-10-01", category="Зарплата", amount=12000.0, op_type="income", description="Зп"),
        TransactionRecord(date="2026-10-02", category="Продукти", amount=400.0, op_type="expense", description="Їжа"),
    ]


@pytest.fixture
def mock_notifier() -> Mock:
    """Фікстура №3: заглушка сповіщувача з налаштованим return_value."""
    notifier = Mock()
    notifier.send.return_value = None
    return notifier