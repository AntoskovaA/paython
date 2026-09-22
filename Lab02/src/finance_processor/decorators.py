from functools import wraps
from time import perf_counter
from typing import Any, Callable


def measure_time(func: Callable) -> Callable:
    """Декоратор для заміру часу виконання функції зі збереженням метаданих через wraps."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"[Таймінг] {func.__name__}: {elapsed:.8f} с")
        return result

    return wrapper