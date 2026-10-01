from finance_domain.dto import TransactionPayload
from finance_domain.models import Category, Expense, FinancialTracker, Income, Transaction
from finance_domain.protocols import BaseReportExporter, Notifier
from finance_domain.repositories import InMemoryRepository
from finance_domain.value_objects import Money


class ConsoleNotifier:
    """Конкретний адаптер для Notifier Protocol (structural subtyping)."""

    def send(self, recipient: str, message: str) -> None:
        print(f"[Сповіщення для {recipient}]: {message}")


class TextReportExporter(BaseReportExporter):
    """Конкретна реалізація BaseReportExporter (nominal subtyping)."""

    def export(self, balance: float, total_income: Money, total_expense: Money) -> str:
        return (
            f"=== Фінансовий Звіт ===\n"
            f"Доходи : {total_income}\n"
            f"Витрати: {total_expense}\n"
            f"Баланс : {balance:.2f} UAH"
        )


class FinanceTrackerService:
    """Сервіс керування трекером із застосуванням Dependency Injection (SOLID DIP)."""

    def __init__(
        self,
        repository: InMemoryRepository[Transaction],
        notifier: Notifier,
        exporter: BaseReportExporter,
    ) -> None:
        self._repo = repository
        self._notifier = notifier
        self._exporter = exporter
        self._tracker = FinancialTracker()

    def create_from_payload(self, payload: TransactionPayload) -> Transaction:
        cat = Category(payload["category"])
        money = Money(payload["amount"])
        tx: Transaction
        if payload["op_type"] == "income":
            tx = Income(payload["id"], payload["date"], cat, money, payload["description"])
        elif payload["op_type"] == "expense":
            tx = Expense(payload["id"], payload["date"], cat, money, payload["description"])
        else:
            raise ValueError(f"Невідомий тип операції: {payload['op_type']}")

        self._repo.add(tx)
        self._tracker.add(tx)
        return tx

    def calculate_summary(self) -> tuple[Money, Money, float]:
        inc = Money(0.0)
        exp = Money(0.0)
        for t in self._tracker:
            if isinstance(t, Income):
                inc = inc + t.money
            elif isinstance(t, Expense):
                exp = exp + t.money
        bal = inc.amount - exp.amount
        return inc, exp, bal

    def generate_report(self, user_email: str) -> str:
        inc, exp, bal = self.calculate_summary()
        report = self._exporter.export(bal, inc, exp)
        self._notifier.send(user_email, f"Звіт сформовано. Підсумковий баланс: {bal:.2f} UAH")
        return report