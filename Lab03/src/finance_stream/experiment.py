import csv
from pathlib import Path
from time import perf_counter
import tracemalloc
from finance_stream.generate_data import generate_dataset
from finance_stream.pipeline import build_finance_pipeline


def run_eager(file_path: Path) -> int:
    with file_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_records = list(reader)  # Повне завантаження всіх записів у пам'ять
    return len([r for r in all_records if r["type"] == "expense"])


def run_lazy(file_path: Path) -> int:
    pipeline = build_finance_pipeline(file_path)
    count = 0
    for r in pipeline:
        if r.op_type == "expense":
            count += 1
    return count


def measure(func, *args) -> tuple[float, float]:
    tracemalloc.start()
    t0 = perf_counter()
    func(*args)
    elapsed = perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return elapsed, peak / (1024 * 1024)


def main() -> None:
    counts = [10_000, 100_000, 500_000]
    print(f"{'Records':<10} | {'Eager time':<12} | {'Lazy time':<12} | {'Eager Peak MB':<14} | {'Lazy Peak MB':<14}")
    print("-" * 72)
    for c in counts:
        p = Path(f"data/test_{c}.csv")
        generate_dataset(p, c)

        t_eag, mem_eag = measure(run_eager, p)
        t_laz, mem_laz = measure(run_lazy, p)

        print(f"{c:<10} | {t_eag:<10.4f} с | {t_laz:<10.4f} с | {mem_eag:<12.2f} MB | {mem_laz:<12.4f} MB")
        p.unlink()


if __name__ == "__main__":
    main()