from pathlib import Path
import pytest
from reliable_finance.models import ProcessingConfig, LoggingConfig, AppConfig


@pytest.fixture
def sample_config(tmp_path: Path) -> AppConfig:
    """Фікстура для створення тестової конфігурації застосунку."""
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