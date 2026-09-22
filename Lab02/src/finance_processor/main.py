from finance_processor.analytics import (
    calculate_balance,
    calculate_category_expenses,
    calculate_sum_of_adjustments,
    create_amount_filter,
    create_transaction_record,
    find_largest_expense,
)
from finance_processor.benchmark import run_benchmark
from finance_processor.data import transactions
from finance_processor.processors import (
    count_category_frequencies,
    create_transaction_index,
    get_unique_categories,
    group_transactions_by_category,
)


def main() -> None:
    print("=== Лабораторна робота № 2: Аналіз фінансового трекера ===")

    # 1. Set comprehension
    unique_cats = get_unique_categories(transactions)
    print("\n[Set comprehension] Унікальні категорії:", unique_cats)

    # 2. Агрегація та декоратор
    balance = calculate_balance(transactions)
    print(f"Розрахований баланс: {balance:.2f} грн")

    # 3. Витрати за категоріями
    cat_exp = calculate_category_expenses(transactions)
    print("\nВитрати за категоріями:", cat_exp)

    # 4. Пошук максимального елемента через lambda
    largest = find_largest_expense(transactions)
    if largest:
        print(f"\n[Lambda] Найбільша витрата: {largest['category']} на суму {largest['amount']} грн")

    # 5. Counter та defaultdict
    freq = count_category_frequencies(transactions)
    print("\n[Counter] Кількість операцій у кожній категорії:", dict(freq))

    grouped = group_transactions_by_category(transactions)
    print("\n[defaultdict] Групування операцій за категоріями:")
    for cat, items in grouped.items():
        print(f"  * {cat}: {len(items)} запис(ів)")

    # 6. Closure
    min_filter = create_amount_filter(1500.0)
    big_items = [t for t in transactions if min_filter(t)]
    print("\n[Closure] Операції на суму >= 1500 грн:")
    for t in big_items:
        print(f"  - {t['date']} | {t['category']} | {t['amount']} грн ({t['type']})")

    # 7. *args та **kwargs
    correction = calculate_sum_of_adjustments(100.0, -25.5, 12.0)
    print(f"\n[*args] Коригування суми: {correction:.2f} грн")

    new_record = create_transaction_record(
        id=8, date="2026-09-20", category="Книги", amount=450.0, type="expense"
    )
    print("[**kwargs] Створено запис:", new_record)

    # 8. Dict comprehension
    index = create_transaction_index(transactions)
    print(f"\n[Dict comprehension] Швидкий доступ до ID=3: {index.get(3)}")

    # Бенчмарк
    run_benchmark()


if __name__ == "__main__":
    main()