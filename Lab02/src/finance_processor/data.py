# Кортеж фіксує незмінні допустимі типи операцій
ALLOWED_TYPES: tuple[str, str] = ("income", "expense")

# Список словників, що представляє вхідний журнал операцій
transactions: list[dict] = [
    {"id": 1, "date": "2026-09-01", "category": "Зарплата", "amount": 28000.0, "type": "income"},
    {"id": 2, "date": "2026-09-02", "category": "Продукти", "amount": 1450.0, "type": "expense"},
    {"id": 3, "date": "2026-09-05", "category": "Транспорт", "amount": 350.0, "type": "expense"},
    {"id": 4, "date": "2026-09-10", "category": "Фриланс", "amount": 5000.0, "type": "income"},
    {"id": 5, "date": "2026-09-12", "category": "Продукти", "amount": 920.0, "type": "expense"},
    {"id": 6, "date": "2026-09-15", "category": "Комунальні", "amount": 2100.0, "type": "expense"},
    {"id": 7, "date": "2026-09-18", "category": "Розваги", "amount": 800.0, "type": "expense"},
]