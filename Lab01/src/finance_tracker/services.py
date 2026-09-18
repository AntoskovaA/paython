from finance_tracker.models import Transaction


def add_transaction(data_list: list[Transaction], item: Transaction) -> None:
    data_list.append(item)


def get_total_income(data_list: list[Transaction]) -> float:
    total = 0.0
    for t in data_list:
        if t.op_type == "income":
            total += t.amount
    return total


def get_total_expense(data_list: list[Transaction]) -> float:
    total = 0.0
    for t in data_list:
        if t.op_type == "expense":
            total += t.amount
    return total


def get_balance(data_list: list[Transaction]) -> float:
    return get_total_income(data_list) - get_total_expense(data_list)


def get_category_expenses(data_list: list[Transaction]) -> dict[str, float]:
    result = {}
    for t in data_list:
        if t.op_type == "expense":
            if t.category in result:
                result[t.category] += t.amount
            else:
                result[t.category] = t.amount
    return result