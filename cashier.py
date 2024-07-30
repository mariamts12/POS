import math
from dataclasses import dataclass, field

from constants import DISCOUNT_ON_RECEIPT, PAYMENT1
from product import Product
from receipt import NewReceipt, NoReceipt, Receipt


@dataclass
class Cashier:
    receipt: Receipt = field(default_factory=NoReceipt)

    def open_receipt(self, number: int) -> None:
        receipt = NewReceipt()
        self.receipt = receipt
        self.receipt.open(number)

    def add_items_to_receipt(self, products: list[Product]) -> None:
        if self.receipt.is_open():
            for item in products:
                self.receipt.add(item)

    def close_receipt(self, payment: str) -> None:
        if payment == PAYMENT1:
            print("Customer paid with cash\n")
        else:
            print("Customer paid with card\n")
        self.receipt.pay(payment)
        self.receipt.close()

    def change_discount(self) -> None:
        percentage = 0
        if is_prime(self.receipt.get_number()):
            percentage = DISCOUNT_ON_RECEIPT
        self.receipt.change_discount(percentage)

    def get_receipt(self) -> Receipt:
        return self.receipt


def is_prime(x: int) -> bool:
    if x < 2:
        return False
    else:
        for i in range(2, int(math.sqrt(x))):
            if x % i == 0:
                return False
    return True
