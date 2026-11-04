class ApplicationError(Exception):
    """Базовий виняток застосунку."""


class ConfigurationError(ApplicationError):
    """Помилка валідації або читання файлу конфігурації."""


class DataError(ApplicationError):
    """Базовий виняток обробки даних."""


class DataImportError(DataError):
    """Помилка відкриття або читання вхідного потоку."""


class RecordValidationError(DataError):
    """Помилка валідації конкретного рядка даних із контекстом."""

    def __init__(
        self,
        message: str,
        *,
        line_number: int | None = None,
        field: str | None = None,
    ) -> None:
        super().__init__(message)
        self.line_number = line_number
        self.field = field


class DataExportError(DataError):
    """Помилка запису або серіалізації вихідних даних."""