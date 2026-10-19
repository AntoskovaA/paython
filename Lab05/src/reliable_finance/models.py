from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    minimum_amount: float
    skip_invalid: bool
    allowed_categories: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str
    path: Path


@dataclass(frozen=True, slots=True)
class AppConfig:
    input_path: Path
    output_path: Path
    processing: ProcessingConfig
    logging: LoggingConfig


@dataclass(frozen=True, slots=True)
class TransactionRecord:
    date: str
    category: str
    amount: float
    op_type: str
    description: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)