from abc import ABC, abstractmethod
from dataclasses import dataclass

from constants import PERCENT


class Product(ABC):
    name: str
    price: float
    discount: int = 0
    amount: int = 1

    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def get_amount(self) -> int:
        return self.amount

    def get_discount(self) -> int:
        return self.discount


@dataclass
class Item(Product):
    name: str
    price: float
    discount: int = 0
    amount: int = 1

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        price = self.price * (1 - (self.discount / PERCENT))
        return round(price, 2)


@dataclass
class Pack(Product):
    product: Product
    amount: int
    discount: int = 0

    def get_name(self) -> str:
        return self.product.get_name()

    def get_price(self) -> float:
        price = self.product.get_price() * self.amount
        price = price * (1 - (self.discount / PERCENT))
        return round(price, 2)
