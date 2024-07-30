from cashier import Cashier
from product import Item


def test_cashier_open_receipt() -> None:
    cashier = Cashier()
    cashier.open_receipt(1)
    receipt = cashier.get_receipt()
    assert receipt.is_open() is True


def test_cashier_close_receipt() -> None:
    cashier = Cashier()
    cashier.open_receipt(1)
    cashier.close_receipt("Cash")
    receipt = cashier.get_receipt()
    assert receipt.is_open() is False


def test_cashier_close_receipt_payment() -> None:
    cashier = Cashier()
    cashier.open_receipt(1)
    cashier.close_receipt("Card")
    receipt = cashier.get_receipt()
    assert receipt.get_payment_type() == "Card"


def test_cashier_add_items() -> None:
    cashier = Cashier()
    cashier.open_receipt(3)
    item1 = Item(name="Something", price=100)
    item2 = Item(name="SomethingToo", price=50)
    cashier.add_items_to_receipt([item1, item2])
    receipt = cashier.get_receipt()
    assert len(receipt.get_items()) == 2


def test_cashier_change_discount() -> None:
    cashier = Cashier()
    cashier.open_receipt(17)
    item = Item(name="Something", price=100)
    cashier.add_items_to_receipt([item])
    previous = cashier.get_receipt().total()
    cashier.change_discount()
    current = cashier.get_receipt().total()
    assert current / previous == 83 / 100
