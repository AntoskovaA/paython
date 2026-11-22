from pathlib import Path
import pytest

from reliable_finance.config import load_config, validate_config
from reliable_finance.exceptions import ConfigurationError
from reliable_finance.logging_config import configure_logging


def test_load_config_success(tmp_path: Path):
    yaml_content = f"""
input:
  path: {tmp_path / 'input.csv'}
output:
  path: {tmp_path / 'output.json'}
processing:
  minimum_amount: 50.0
  skip_invalid: true
  allowed_categories:
    - Зарплата
logging:
  level: DEBUG
  path: {tmp_path / 'app.log'}
"""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml_content, encoding="utf-8")
    
    # Створюємо вхідний файл, щоб проходить перевірка existence
    (tmp_path / "input.csv").write_text("date,category,amount,type,description\n", encoding="utf-8")

    cfg = load_config(config_file)
    assert cfg.processing.minimum_amount == 50.0
    assert cfg.logging.level == "DEBUG"


def test_validate_config_negative_amount(sample_config):
    # Змінюємо minimum_amount на від'ємне значення
    bad_processing = sample_config.processing.__class__(
        minimum_amount=-10.0,
        skip_invalid=True,
        allowed_categories=("Зарплата",),
    )
    bad_cfg = sample_config.__class__(
        input_path=sample_config.input_path,
        output_path=sample_config.output_path,
        processing=bad_processing,
        logging=sample_config.logging,
    )
    with pytest.raises(ConfigurationError, match="minimum_amount"):
        validate_config(bad_cfg)


def test_configure_logging(tmp_path: Path):
    log_file = tmp_path / "logs" / "test.log"
    configure_logging("INFO", log_file)
    assert log_file.parent.exists()