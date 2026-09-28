from itertools import islice
from pathlib import Path
from finance_stream.analytics import stream_cumulative_balance, stream_financial_summary
from finance_stream.batches import batched_transactions
from finance_stream.filters import filter_expenses_by_threshold
from finance_stream.generate_data import generate_dataset
from finance_stream.models import TransactionLimitIterator
from finance_stream.pipeline import build_finance_pipeline


def main() -> None:
    csv_file = Path("data/transactions_sample.csv")
    if not csv_file.exists():
        generate_dataset(csv_file, 1000)

    print("=== Лабораторна робота № 3: Потоковий конвеєр (Варіант 12) ===")

    # 1. Перші 5 елементів через itertools.islice
    print("\n--- Перші 5 операцій (itertools.islice) ---")
    p1 = build_finance_pipeline(csv_file)
    for tx in islice(p1, 5):
        print(f"{tx.date} | {tx.op_type.upper():7} | {tx.category:12} | {tx.amount:8.2f} грн | {tx.description}")

    # 2. Generator expression
    p2 = build_finance_pipeline(csv_file)
    total_exp_gen = sum(t.amount for t in p2 if t.op_type == "expense")
    print(f"\n[Generator expression] Загальні витрати: {total_exp_gen:.2f} грн")

    # 3. Фільтрація витрат за порогом
    p3 = build_finance_pipeline(csv_file)
    large_food = list(islice(filter_expenses_by_threshold(p3, "Продукти", 1500.0), 3))
    print(f"\n[Filter & islice] Витрати на 'Продукти' >= 1500 грн (знайдено {len(large_food)})")

    # 4. Батчинг
    p4 = build_finance_pipeline(csv_file)
    batch_gen = batched_transactions(p4, batch_size=250)
    first_batch = next(batch_gen)
    print(f"\n[Batching] Розмір першого батча: {len(first_batch)} записів")

    # 5. Кумулятивний баланс (itertools.accumulate)
    p5 = build_finance_pipeline(csv_file)
    first_cum = list(islice(stream_cumulative_balance(p5), 5))
    print("\n[itertools.accumulate] Кумулятивний баланс перших 5 операцій:", [round(x, 2) for x in first_cum])

    # 6. Власний ітератор
    p6 = build_finance_pipeline(csv_file)
    sample_list = list(islice(p6, 10))
    custom_iter = TransactionLimitIterator(sample_list, max_count=2)
    print("\n[Custom Iterator] Перші записи через TransactionLimitIterator:")
    for item in custom_iter:
        print(f"  * {item.category}: {item.amount} грн")

    # 7. Підсумкова статистика
    p7 = build_finance_pipeline(csv_file)
    stats = stream_financial_summary(p7)
    print("\n--- Фінансова статистика потоку ---")
    print(f"Доходи  : {stats['total_income']:.2f} грн")
    print(f"Витрати : {stats['total_expense']:.2f} грн")
    print(f"Баланс  : {stats['balance']:.2f} грн")


if __name__ == "__main__":
    main()