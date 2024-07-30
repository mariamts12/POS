from dataclasses import dataclass, field

from constants import RECEIPT_HEADERS, REVENUE_HEADERS, SALES_HEADERS
from logger import Logger
from product import Product
from product_dao import ProductDAO
from receipt import Receipt
from report_dao import XReportDAO, ZReportDAO


@dataclass
class Store:
    database: str
    shift: int = 0
    customer: int = 0
    logger: Logger = field(default_factory=Logger)

    def __post_init__(self) -> None:
        product_dao = ProductDAO(self.database)
        product_dao.create()
        self.products = product_dao.get()
        product_dao.disconnect()
        self.x_report_dao = XReportDAO(self.database)
        self.z_report_dao = ZReportDAO(self.database)
        self.x_report_dao.create()
        self.z_report_dao.create()

    def get_products(self) -> list[Product]:
        return self.products

    def get_customer_count(self) -> int:
        return self.customer

    def get_shift_count(self) -> int:
        return self.shift

    def start_new_shift(self) -> None:
        self.shift += 1

    def new_customer(self) -> None:
        self.customer += 1

    def print_products(self) -> None:
        products: list[list[object]]
        products = [
            [i.get_name(), i.get_price(), i.get_amount(), i.get_discount()]
            for i in self.products
        ]
        self.logger.print_table(products, RECEIPT_HEADERS)

    def make_x_report(self) -> None:
        report = self.x_report_dao.get()
        self.logger.print_table(report[0], SALES_HEADERS)
        self.logger.print_table(report[1], REVENUE_HEADERS)

    def make_z_report(self) -> None:
        self.z_report_dao.update_sales()
        self.z_report_dao.update_revenue()
        self.x_report_dao.clear()
        report = self.z_report_dao.get()
        self.logger.print_table(report[0], SALES_HEADERS)
        self.logger.print_table(report[1], REVENUE_HEADERS)

    def update_x(self, receipt: Receipt) -> None:
        self.x_report_dao.update_sales(receipt.get_items())
        self.x_report_dao.update_revenue(receipt.get_payment_type(), receipt.total())

    def close_store(self) -> None:
        self.x_report_dao.disconnect()
        self.z_report_dao.disconnect()

    def print_receipt(self, receipt: Receipt) -> None:
        products: list[list[object]]
        products = [
            [
                i.get_name(),
                i.get_amount(),
                round(
                    (i.get_price() * 100 / (100 - i.get_discount())) / i.get_amount(), 2
                ),
                i.get_price(),
            ]
            for i in receipt.get_items()
        ]
        products.append(["", "", "", receipt.total()])
        self.logger.print_table(products, RECEIPT_HEADERS)
