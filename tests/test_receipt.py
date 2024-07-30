from constants import PAYMENT1
from product import Item, Pack
from receipt import NewReceipt


def test_open() -> None:
    receipt = NewReceipt()
    receipt.open(1)
    assert receipt.is_open() is True


def test_open_get_number() -> None:
    receipt = NewReceipt()
    receipt.open(3)
    assert receipt.get_number() == 3


def test_close() -> None:
    receipt = NewReceipt()
    receipt.close()
    assert receipt.is_open() is False


def test_add() -> None:
    receipt = NewReceipt()
    receipt.add(Item(name="Milk", price=4.99))
    assert len(receipt.get_items()) == 1


def test_add_two() -> None:
    receipt = NewReceipt()
    item = Item(name="Milk", price=4.99)
    receipt.add(item)
    receipt.add(Pack(product=item, amount=6))
    assert len(receipt.get_items()) == 2


def test_pay() -> None:
    receipt = NewReceipt()
    item = Item(name="Milk", price=4.99)
    receipt.add(Pack(product=item, amount=6))
    receipt.pay(PAYMENT1)
    assert receipt.get_payment_type() == PAYMENT1


def test_total() -> None:
    receipt = NewReceipt()
    item = Item(name="Milk", price=5)
    receipt.add(item)
    receipt.add(Pack(product=item, amount=6))
    item = Item(name="Bread", price=1.99)
    receipt.add(item)
    assert receipt.total() == 36.99


def test_change_discount() -> None:
    receipt = NewReceipt()
    item = Item(name="Milk", price=5)
    receipt.add(Pack(product=item, amount=6))
    receipt.change_discount(20)
    assert receipt.total() == 24
