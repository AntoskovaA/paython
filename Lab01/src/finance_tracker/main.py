from datetime import date, datetime
from finance_tracker.models import Transaction, ValidationError
from finance_tracker.services import (
    add_transaction,
    get_balance,
    get_category_expenses,
    get_total_expense,
    get_total_income,
)


def demo_data() -> list[Transaction]:
    return [
        Transaction(date(2026, 9, 1), "Зарплата", 28000.0, "income"),
        Transaction(date(2026, 9, 2), "Продукти", 1450.0, "expense"),
        Transaction(date(2026, 9, 5), "Транспорт", 350.0, "expense"),
        Transaction(date(2026, 9, 10), "Фриланс", 5000.0, "income"),
        Transaction(date(2026, 9, 12), "Продукти", 920.0, "expense"),
    ]


def show_transactions(items: list[Transaction]) -> None:
    if not items:
        print("\nСписок операцій порожній.")
        return

    print("\n--- Список операцій ---")
    print(f"{'Дата':12} | {'Тип':8} | {'Категорія':15} | {'Сума':10}")
    print("-" * 52)
    for t in items:
        print(f"{str(t.op_date):12} | {t.op_type:8} | {t.category:15} | {t.amount:10.2f} грн")


def add_new_transaction(items: list[Transaction]) -> None:
    print("\n--- Нова операція ---")
    raw_date = input("Дата (РРРР-ММ-ДД, Enter - сьогодні): ").strip()
    try:
        t_date = datetime.strptime(raw_date, "%Y-%m-%d").date() if raw_date else date.today()
    except ValueError:
        print("Помилка: невірний формат дати!")
        return

    t_type_num = input("Тип (1 - income, 2 - expense): ").strip()
    if t_type_num == "1":
        t_type = "income"
    elif t_type_num == "2":
        t_type = "expense"
    else:
        print("Помилка: оберіть 1 або 2!")
        return

    cat = input("Категорія: ").strip()
    try:
        amt = float(input("Сума: ").strip())
        new_tx = Transaction(t_date, cat, amt, t_type)
        add_transaction(items, new_tx)
        print("Транзакцію успішно додано!")
    except ValueError:
        print("Помилка: сума має бути числом!")
    except ValidationError as err:
        print(f"Помилка валідації: {err}")


def show_statistics(items: list[Transaction]) -> None:
    inc = get_total_income(items)
    exp = get_total_expense(items)
    bal = get_balance(items)
    cat_exp = get_category_expenses(items)

    print("\n--- Фінансова статистика ---")
    print(f"Доходи : {inc:.2f} грн")
    print(f"Витрати: {exp:.2f} грн")
    print(f"Баланс : {bal:.2f} грн")
    print("\nВитрати за категоріями:")
    for cat, val in cat_exp.items():
        print(f"  * {cat}: {val:.2f} грн")


def main() -> None:
    tx_list = demo_data()

    while True:
        print("\n=== Меню Фінансового трекера ===")
        print("1. Всі операції")
        print("2. Додати операцію")
        print("3. Баланс і статистика")
        print("4. Вихід")

        choice = input("Ваш вибір (1-4): ").strip()
        if choice == "1":
            show_transactions(tx_list)
        elif choice == "2":
            add_new_transaction(tx_list)
        elif choice == "3":
            show_statistics(tx_list)
        elif choice == "4":
            print("Вихід з програми.")
            break
        else:
            print("Невідома команда!")


if __name__ == "__main__":
    main()