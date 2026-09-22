from time import perf_counter


def run_benchmark() -> None:
    sizes = [1_000, 10_000, 100_000]
    print("\n--- Результати експериментального Benchmark ---")
    print(f"{'Кількість records':<18} | {'list search (с)':<18} | {'dict search (с)':<18}")
    print("-" * 60)

    for size in sizes:
        dataset = [
            {"id": i, "category": "Тест", "amount": 100.0, "type": "expense"}
            for i in range(size)
        ]
        index = {item["id"]: item for item in dataset}
        target_id = size - 1  # Пошук останнього елемента (найгірший сценарій)

        # Лінійний пошук у списку O(n)
        t_start = perf_counter()
        _ = next((x for x in dataset if x["id"] == target_id), None)
        t_list = perf_counter() - t_start

        # Хеш-пошук у словнику O(1)
        t_start = perf_counter()
        _ = index.get(target_id)
        t_dict = perf_counter() - t_start

        print(f"{size:<18} | {t_list:<18.8f} | {t_dict:<18.8f}")