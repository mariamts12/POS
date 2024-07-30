import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from sqlite3 import Connection
from typing import Tuple

from constants import (
    X_REVENUE_TABLE_NAME,
    X_SALES_TABLE_NAME,
    Z_REVENUE_TABLE_NAME,
    Z_SALES_TABLE_NAME,
)
from product import Product


@dataclass
class AbstractDAO(ABC):
    database: str
    tables: list[str] = field(default_factory=list)
    fields: list[str] = field(default_factory=list)

    @abstractmethod
    def __post_init__(self) -> None:
        self.connection = self.connect()

    def connect(self) -> Connection:
        return sqlite3.connect(self.database)

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()

    def _create(self) -> None:
        cursor = self.connection.cursor()

        for i in range(len(self.tables)):
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS " + self.tables[i] + self.fields[i]
            )

    def get(self) -> Tuple[list[list[object]], list[list[object]]]:
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM " + self.tables[0] + " WHERE Sales <> 0")
        result = cursor.fetchall()

        sales: list[list[object]] = []
        for product, amount in result:
            sales.append([product, amount])

        cursor.execute("SELECT * FROM " + self.tables[1])
        result = cursor.fetchall()

        revenue: list[list[object]] = []
        for payment, amount in result:
            revenue.append([payment, amount])

        report = (sales, revenue)
        return report

    def create(self) -> None:
        self._create()
        with self.connection:
            cursor = self.connection.cursor()
            products = cursor.execute(
                "SELECT Product FROM Store" " GROUP BY Product"
            ).fetchall()
            result = cursor.execute("SELECT * FROM " + self.tables[0]).fetchall()
            if len(result) == 0:
                for item in products:
                    cursor.execute(
                        "INSERT INTO " + self.tables[0] + " VALUES(?, ?)", (item[0], 0)
                    )

            result = cursor.execute("SELECT * FROM " + self.tables[1]).fetchall()
            if len(result) == 0:
                cursor.execute(
                    "INSERT INTO " + self.tables[1] + " VALUES(?,?)", ("Cash", 0)
                )
                cursor.execute(
                    "INSERT INTO " + self.tables[1] + " VALUES(?,?)", ("Card", 0)
                )
            self.connection.commit()

    def _update_revenue_row(self, args: Tuple[str, float]) -> None:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE "
                + self.tables[1]
                + " SET Revenue = Revenue + ? WHERE Payment = ?",
                (round(args[1], 2), args[0]),
            )
            self.connection.commit()

    def _update_sales_row(self, args: Tuple[str, int]) -> None:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE " + self.tables[0] + " SET Sales = Sales + ? WHERE Product = ?",
                (args[1], args[0]),
            )
            self.connection.commit()

    def clear(self) -> None:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE " + self.tables[0] + " SET Sales = 0")
            cursor.execute("UPDATE " + self.tables[1] + " SET Revenue = 0")
            self.connection.commit()


@dataclass
class XReportDAO(AbstractDAO):
    database: str

    def __post_init__(self) -> None:
        self.connection = self.connect()
        self.tables = [X_SALES_TABLE_NAME, X_REVENUE_TABLE_NAME]
        fields1 = "(Product TEXT NOT NULL PRIMARY KEY, Sales INTEGER)"
        fields2 = "(Payment TEXT NOT NULL PRIMARY KEY, Revenue FLOAT)"
        self.fields = [fields1, fields2]

    def update_sales(self, items: list[Product]) -> None:
        for i in items:
            self._update_sales_row((i.get_name(), i.get_amount()))

    def update_revenue(self, payment: str, amount: float) -> None:
        self._update_revenue_row((payment, amount))


@dataclass
class ZReportDAO(AbstractDAO):
    database: str

    def __post_init__(self) -> None:
        self.connection = self.connect()
        self.tables = [Z_SALES_TABLE_NAME, Z_REVENUE_TABLE_NAME]
        fields1 = "(Product TEXT NOT NULL PRIMARY KEY, Sales INTEGER)"
        fields2 = "(Payment TEXT NOT NULL PRIMARY KEY, Revenue FLOAT)"
        self.fields = [fields1, fields2]

    def update_revenue(self) -> None:
        with self.connection:
            cursor = self.connection.cursor()
            result = cursor.execute("SELECT * FROM XRevenue").fetchall()
            self._update_revenue_row(result[0])
            self._update_revenue_row(result[1])

    def update_sales(self) -> None:
        with self.connection:
            cursor = self.connection.cursor()
            result = cursor.execute("SELECT * FROM XSales").fetchall()
            for i in range(len(result)):
                self._update_sales_row(result[i])
