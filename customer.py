import random
from dataclasses import dataclass, field
from typing import Protocol

from constants import MAX_ITEMS_IN_CART, MIN_ITEMS_IN_CART, PAYMENT1, PAYMENT2
from product import Product


class Customer(Protocol):
    def choose_items(self, products: list[Product]) -> None:
        pass

    def choose_payment(self) -> str:
        pass


@dataclass
class RandomChoiceCustomer:
    def __post_init__(self) -> None:
        self.payment = [PAYMENT1, PAYMENT2]
        self.cart: list[Product] = []

    def choose_items(self, products: list[Product]) -> list[Product]:
        rand = random.randint(MIN_ITEMS_IN_CART, MAX_ITEMS_IN_CART)
        for i in range(rand):
            rand2 = random.randint(0, len(products) - 1)
            self.cart.append(products[rand2])
        return self.cart

    def choose_payment(self) -> str:
        rand = random.randint(0, 1)
        return self.payment[rand]


@dataclass
class DeterministicCustomer:
    items: list[int] = field(default_factory=list)
    payment_type: int = 0

    def __post_init__(self) -> None:
        self.payment = [PAYMENT1, PAYMENT2]
        self.cart: list[Product] = []

    def choose_items(self, products: list[Product]) -> list[Product]:
        for i in self.items:
            self.cart.append(products[i])
        return self.cart

    def choose_payment(self) -> str:
        return self.payment[self.payment_type]
