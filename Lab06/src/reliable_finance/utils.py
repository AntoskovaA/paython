from collections.abc import Generator
from contextlib import contextmanager
import logging
from time import perf_counter

logger = logging.getLogger("reliable_finance.utils")


@contextmanager
def logged_operation(operation_name: str) -> Generator[None, None, None]:
    """Власний контекстний менеджер для фіксації тривалості операції та безпеки."""
    logger.info(">>> Початок операції: %s", operation_name)
    start_time = perf_counter()
    try:
        yield
    except Exception:
        logger.exception("!!! Збій під час операції: %s", operation_name)
        raise
    else:
        elapsed = perf_counter() - start_time
        logger.info("<<< Операцію '%s' успішно завершено за %.6f с", operation_name, elapsed)