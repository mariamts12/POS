import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Protocol

from constants import STORE_TABLE_NAME
from product import Item, Pack, Product


class DAO(Protocol):
    def connect(self) -> Connection:
        pass

    def disconnect(self) -> None:
        pass

    def create(self) -> None:
        pass

    def get(self) -> object:
        pass


@dataclass
class ProductDAO:
    database: str

    def __post_init__(self) -> None:
        self.connection = self.connect()
        fields = (
            "(Product TEXT NOT NULL, "
            "Price FLOAT, "
            "Units INTEGER, "
            "Discount INTEGER REAL CHECK (discount >= 0 AND discount <= 100), "
            "PRIMARY KEY (Product, Units))"
        )
        self.fields = fields
        self.table = STORE_TABLE_NAME

    def connect(self) -> Connection:
        return sqlite3.connect(self.database)

    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()

    def create(self) -> None:
        cursor = self.connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS " + self.table + self.fields)

    def get(self) -> list[Product]:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM store")
            result = cursor.fetchall()
            store: list[Product] = []
            for product in result:
                if product[2] > 1:
                    item = Item(name=product[0], price=product[1])
                    pack = Pack(amount=product[2], product=item, discount=product[3])
                    store.append(pack)
                else:
                    item = Item(name=product[0], price=product[1], discount=product[3])
                    store.append(item)
        return store

    def update(self, args: list[object]) -> None:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO Store (Product, Price, Units, Discount)"
                " VALUES (?, ?, ?, ?)",
                (args[0], args[1], args[2], args[3]),
            )
            self.connection.commit()

    def clear(self) -> None:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("DROP TABLE " + self.table)
            self.connection.commit()
