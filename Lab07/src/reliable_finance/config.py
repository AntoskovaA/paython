from pathlib import Path
import yaml
from reliable_finance.exceptions import ConfigurationError
from reliable_finance.models import AppConfig, LoggingConfig, ProcessingConfig


def load_config(path: Path) -> AppConfig:
    """Завантаження та сувора валідація YAML конфігурації (Fail-fast)."""
    try:
        with path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
    except FileNotFoundError as error:
        raise ConfigurationError(f"Конфігураційний файл не знайдено: {path}") from error
    except yaml.YAMLError as error:
        raise ConfigurationError("Некоректний синтаксис файлу YAML") from error

    try:
        config = AppConfig(
            input_path=Path(raw["input"]["path"]),
            output_path=Path(raw["output"]["path"]),
            processing=ProcessingConfig(
                minimum_amount=float(raw["processing"]["minimum_amount"]),
                skip_invalid=bool(raw["processing"]["skip_invalid"]),
                allowed_categories=tuple(raw["processing"]["allowed_categories"]),
            ),
            logging=LoggingConfig(
                level=str(raw["logging"]["level"]),
                path=Path(raw["logging"]["path"]),
            ),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ConfigurationError("Помилка структури YAML: відсутні або некоректні ключі") from error

    validate_config(config)
    return config


def validate_config(config: AppConfig) -> None:
    if config.processing.minimum_amount < 0:
        raise ConfigurationError("minimum_amount не може бути від'ємною!")
    if not config.input_path.exists():
        raise ConfigurationError(f"Вхідний файл не знайдено: {config.input_path}")
    if not config.processing.allowed_categories:
        raise ConfigurationError("Список allowed_categories не може бути порожнім!")