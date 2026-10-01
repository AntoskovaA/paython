from finance_domain.dto import TransactionPayload
from finance_domain.models import Transaction
from finance_domain.repositories import InMemoryRepository
from finance_domain.services import ConsoleNotifier, FinanceTrackerService, TextReportExporter

def main() -> None:
    print("=== Лабораторна робота № 4: Професійне ООП (Варіант 12) ===")

    # Створення залежностей (Dependency Injection)
    repo = InMemoryRepository[Transaction]()
    notifier = ConsoleNotifier()
    exporter = TextReportExporter()

    service = FinanceTrackerService(repository=repo, notifier=notifier, exporter=exporter)

    # Демонстрація створення операцій через TypedDict payload
    sample_payloads: list[TransactionPayload] = [
        {"id": 1, "date": "2026-10-01", "category": "Зарплата", "amount": 32000.0, "op_type": "income", "description": "Основна з/п"},
        {"id": 2, "date": "2026-10-02", "category": "Продукти", "amount": 1650.0, "op_type": "expense", "description": "Супермаркет"},
        {"id": 3, "date": "2026-10-03", "category": "Оренда", "amount": 8500.0, "op_type": "expense", "description": "Житло"},
        {"id": 4, "date": "2026-10-04", "category": "Фриланс", "amount": 6000.0, "op_type": "income", "description": "Проєктний бонус"},
    ]

    for item in sample_payloads:
        tx = service.create_from_payload(item)
        print(f"Створено: {tx}")

    print("\n--- Перевірка роботи репозиторію та контейнера ---")
    print(f"Кількість операцій у репозиторії: {len(repo.all())}")
    found = repo.get(2)
    print(f"Пошук операції за ID=2: {found}")

    print("\n--- Генерація фінансового звіту (DIP & Notifier) ---")
    report = service.generate_report("alina@example.com")
    print(report)

if __name__ == "__main__":
    main()