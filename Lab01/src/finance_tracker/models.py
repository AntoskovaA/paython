from dataclasses import dataclass
from datetime import date


class ValidationError(Exception):
    """Помилка валідації вхідних даних"""
    pass


@dataclass
class Transaction:
    op_date: date
    category: str
    amount: float
    op_type: str  # "income" або "expense"

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValidationError("Сума повинна бути більшою за нуль!")
        if self.op_type not in ("income", "expense"):
            raise ValidationError("Тип має бути тільки income або expense!")
        if not self.category.strip():
            raise ValidationError("Категорія не може бути порожньою!")
        self.category = self.category.strip()