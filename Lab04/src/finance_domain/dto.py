from typing import TypedDict


class TransactionPayload(TypedDict):
    id: int
    date: str
    category: str
    amount: float
    op_type: str
    description: str