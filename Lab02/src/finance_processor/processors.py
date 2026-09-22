from collections import Counter, defaultdict


def get_unique_categories(items: list[dict]) -> set[str]:
    """Set comprehension: формування множини унікальних категорій."""
    return {item["category"] for item in items}


def create_transaction_index(items: list[dict]) -> dict[int, dict]:
    """Dict comprehension: швидкий індекс пошуку транзакцій за ID."""
    return {item["id"]: item for item in items}


def group_transactions_by_category(items: list[dict]) -> dict[str, list[dict]]:
    """Групування операцій за категоріями з використанням defaultdict."""
    grouped = defaultdict(list)
    for item in items:
        grouped[item["category"]].append(item)
    return dict(grouped)


def count_category_frequencies(items: list[dict]) -> Counter:
    """Підрахунок частоти появи кожної категорії за допомогою Counter."""
    return Counter(item["category"] for item in items)


def filter_by_type(items: list[dict], op_type: str) -> list[dict]:
    """List comprehension: фільтрація операцій за типом."""
    return [item for item in items if item["type"] == op_type]