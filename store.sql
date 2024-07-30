CREATE TABLE IF NOT EXISTS Store(
            Product TEXT NOT NULL,
            Price FLOAT,
            Units INTEGER,
            Discount INTEGER REAL CHECK (Discount >= 0 AND Discount <= 100),
            PRIMARY KEY (Product, Units));


INSERT OR REPLACE INTO Store (Product, Price, Units, Discount)
    VALUES
            ('Bread', 1.99, 1, 0),
            ('Milk', 4.99, 1, 0),
            ('Mineral Water', 3, 1, 0),
            ('Mineral Water', 3, 6, 10);
