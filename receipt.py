from dataclasses import dataclass, field
from typing import Protocol

from constants import PERCENT
from product import Product


class Receipt(Protocol):
    def open(self, number: int) -> None:
        pass

    def close(self) -> None:
        pass

    def add(self, product: Product) -> None:
        pass

    def pay(self, payment: str) -> None:
        pass

    def is_open(self) -> bool:
        pass

    def change_discount(self, discount: int) -> None:
        pass

    def get_number(self) -> int:
        pass

    def total(self) -> float:
        pass

    def get_payment_type(self) -> str:
        pass

    def get_items(self) -> list[Product]:
        pass


@dataclass
class NoReceipt(Receipt):
    pass


@dataclass
class NewReceipt:
    number: int = 0
    is_receipt_open: bool = False
    items: list[Product] = field(default_factory=list)
    discount: int = 0
    payment: str = ""

    def open(self, number: int) -> None:
        self.is_receipt_open = True
        self.number = number

    def close(self) -> None:
        self.is_receipt_open = False

    def add(self, product: Product) -> None:
        self.items.append(product)

    def is_open(self) -> bool:
        return self.is_receipt_open

    def change_discount(self, discount: int) -> None:
        self.discount = discount

    def get_number(self) -> int:
        return self.number

    def total(self) -> float:
        total = 0.0
        for product in self.items:
            total += product.get_price()
        total = total * (1 - (self.discount / PERCENT))
        return round(total, 2)

    def pay(self, payment: str) -> None:
        self.payment = payment

    def get_payment_type(self) -> str:
        return self.payment

    def get_items(self) -> list[Product]:
        return self.items
