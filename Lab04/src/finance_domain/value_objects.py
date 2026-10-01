from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Money:
    amount: float
    currency: str = "UAH"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Сума грошей не може бути від'ємною!")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Неможливо додавати різні валюти!")
        return Money(round(self.amount + other.amount, 2), self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Неможливо віднімати різні валюти!")
        if self.amount < other.amount:
            raise ValueError("Результат операції не може бути від'ємним!")
        return Money(round(self.amount - other.amount, 2), self.currency)

    def __lt__(self, other: "Money") -> bool:
        if self.currency != other.currency:
            raise ValueError("Неможливо порівнювати різні валюти!")
        return self.amount < other.amount

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"