from typing import Tuple

from constants import TEST_DATABASE
from product import Item
from product_dao import ProductDAO
from report_dao import XReportDAO, ZReportDAO

DATA = [
    ["Bread", 1.99, 1, 0],
    ["Milk", 4.99, 1, 0],
    ["Mineral Water", 3, 1, 0],
    ["Mineral Water", 3, 6, 10],
]

REPORT_AFTER_SET_UP: Tuple[list[list[object]], list[list[object]]] = (
    [],
    [["Cash", 0.0], ["Card", 0.0]],
)

REPORT_AFTER_UPDATE = ([["Bread", 1]], [["Cash", 15.5], ["Card", 0.0]])


def create_and_update_store() -> ProductDAO:
    product_dao = ProductDAO(TEST_DATABASE)
    product_dao.create()
    product_dao.update(DATA[0])
    product_dao.update(DATA[1])
    product_dao.update(DATA[2])
    product_dao.update(DATA[3])
    return product_dao


def create_x() -> XReportDAO:
    x_dao = XReportDAO(TEST_DATABASE)
    x_dao.create()
    return x_dao


def create_z() -> ZReportDAO:
    z_report = ZReportDAO(TEST_DATABASE)
    z_report.create()
    return z_report


def test_get_products() -> None:
    product_dao = create_and_update_store()
    list_of_products = product_dao.get()
    product_dao.clear()
    product_dao.disconnect()
    products = [
        [
            i.get_name(),
            (i.get_price() * 100 / (100 - i.get_discount())) / i.get_amount(),
            i.get_amount(),
            i.get_discount(),
        ]
        for i in list_of_products
    ]
    assert products == DATA


def test_get_x_report() -> None:
    product_dao = create_and_update_store()
    x_dao = create_x()
    report = x_dao.get()
    product_dao.clear()
    product_dao.disconnect()
    x_dao.clear()
    x_dao.disconnect()
    assert report == REPORT_AFTER_SET_UP


def test_update_x() -> None:
    product_dao = create_and_update_store()
    x_dao = create_x()
    x_dao.update_revenue("Cash", 15.5)
    item = Item(name="Bread", price=1.99, amount=1, discount=0)
    x_dao.update_sales([item])
    report = x_dao.get()
    product_dao.clear()
    product_dao.disconnect()
    x_dao.clear()
    x_dao.disconnect()
    assert report == REPORT_AFTER_UPDATE


def test_get_z_report() -> None:
    product_dao = create_and_update_store()
    z_dao = create_z()
    report = z_dao.get()
    product_dao.clear()
    product_dao.disconnect()
    z_dao.clear()
    z_dao.disconnect()
    assert report == REPORT_AFTER_SET_UP


def test_update_z() -> None:
    product_dao = create_and_update_store()
    x_dao = create_x()
    z_dao = create_z()
    x_dao.update_revenue("Cash", 15.5)
    item = Item(name="Bread", price=1.99, amount=1, discount=0)
    x_dao.update_sales([item])
    z_dao.update_sales()
    z_dao.update_revenue()
    report = z_dao.get()
    product_dao.clear()
    product_dao.disconnect()
    x_dao.clear()
    x_dao.disconnect()
    z_dao.clear()
    z_dao.disconnect()
    assert report == REPORT_AFTER_UPDATE
