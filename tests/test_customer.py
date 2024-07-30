from constants import PAYMENT1, PAYMENT2
from customer import DeterministicCustomer, RandomChoiceCustomer
from product import Item, Pack


def test_choose_items() -> None:
    customer = DeterministicCustomer(items=[0, 1, 0])
    item1 = Item(name="Mineral Water", price=3.0, amount=1)
    item2 = Pack(product=item1, amount=6, discount=20)
    items = customer.choose_items([item1, item2])
    assert items == [item1, item2, item1]


def test_choose_payment() -> None:
    customer = DeterministicCustomer(payment_type=1)
    assert customer.choose_payment() == PAYMENT2


def test_random_choose_payment() -> None:
    customer = RandomChoiceCustomer()
    assert customer.choose_payment() in [PAYMENT1, PAYMENT2]
