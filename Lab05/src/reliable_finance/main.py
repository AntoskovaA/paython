import logging
from pathlib import Path
from reliable_finance.config import load_config
from reliable_finance.exceptions import ApplicationError
from reliable_finance.exporters import atomic_export_json
from reliable_finance.logging_config import configure_logging
from reliable_finance.services import (
    ImportStatistics,
    filter_by_minimum_amount,
    import_transactions,
)
from reliable_finance.utils import logged_operation

logger = logging.getLogger("reliable_finance.main")


def main() -> None:
    config_path = Path("config.yaml")

    try:
        config = load_config(config_path)
        configure_logging(config.logging.level, config.logging.path)

        statistics = ImportStatistics()

        with logged_operation("Імпорт, валідація та експорт фінансових транзакцій"):
            # Потоковий конвеєр
            stream = import_transactions(
                config.input_path,
                skip_invalid=config.processing.skip_invalid,
                allowed_categories=config.processing.allowed_categories,
                statistics=statistics,
            )

            filtered = filter_by_minimum_amount(
                stream,
                config.processing.minimum_amount,
            )

            exported_count = atomic_export_json(filtered, config.output_path)

        logger.info(
            "Статистика обробки: Всього=%d | Валідних=%d | Некоректних=%d | Експортовано=%d",
            statistics.total,
            statistics.valid,
            statistics.invalid,
            exported_count,
        )

    except ApplicationError as error:
        logger.error("Критична помилка виконання застосунку: %s", error)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()