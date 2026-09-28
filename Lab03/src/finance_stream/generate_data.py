import csv
import random
from pathlib import Path

INCOME_CATS = ("Зарплата", "Фриланс", "Інвестиції", "Кешбек")
EXPENSE_CATS = ("Продукти", "Транспорт", "Комунальні", "Розваги", "Одяг", "Здоров'я")


def generate_dataset(file_path: Path, count: int) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "category", "amount", "type", "description"])
        for i in range(1, count + 1):
            if random.random() < 0.3:
                op_type = "income"
                cat = random.choice(INCOME_CATS)
                amt = round(random.uniform(500, 30000), 2)
            else:
                op_type = "expense"
                cat = random.choice(EXPENSE_CATS)
                amt = round(random.uniform(50, 4000), 2)

            writer.writerow([
                f"2026-09-{(i % 28) + 1:02d}",
                cat,
                amt,
                op_type,
                f"Операція №{i}",
            ])


if __name__ == "__main__":
    generate_dataset(Path("data/transactions_sample.csv"), 1000)
    print("Згенеровано базовий датасет data/transactions_sample.csv")