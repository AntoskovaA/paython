from abc import ABC, abstractmethod
from typing import Protocol
from finance_domain.value_objects import Money


class Notifier(Protocol):
    """Structural typing (Protocol) для надсилання повідомлень/сповіщень."""

    def send(self, recipient: str, message: str) -> None:
        ...


class BaseReportExporter(ABC):
    """Nominal typing (ABC) для експорту фінансового звіту."""

    @abstractmethod
    def export(self, balance: float, total_income: Money, total_expense: Money) -> str:
        ...