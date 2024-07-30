from product import Item, Pack, Product


def create_item() -> Product:
    return Item(name="Bread", price=2, amount=1, discount=25)


def test_item_get_name() -> None:
    assert create_item().get_name() == "Bread"


def test_item_get_price() -> None:
    assert create_item().get_price() == 1.5


def test_item_get_amount() -> None:
    assert create_item().get_amount() == 1


def test_item_get_discount() -> None:
    assert create_item().get_discount() == 25


def create_pack() -> Product:
    item = Item(name="Mineral Water", price=3.0, amount=1)
    return Pack(product=item, amount=6, discount=20)


def test_pack_get_name() -> None:
    assert create_pack().get_name() == "Mineral Water"


def test_pack_get_price() -> None:
    assert create_pack().get_price() == 14.4


def test_pack_get_amount() -> None:
    assert create_pack().get_amount() == 6


def test_pack_get_discount() -> None:
    assert create_pack().get_discount() == 20
