import sqlite3
from rich.console import Console
from rich.table import Table

console = Console()

# Open a connection to the database
connection = sqlite3.connect('./src/db/database.sqlite')

# Create a cursor
cursor = connection.cursor()


def create_table():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)")


def insert(item, quantity, price):
    cursor.execute("INSERT INTO store VALUES (?, ?, ?)",
                   (item, quantity, price))
    connection.commit()


def insert_many(items):
    cursor.executemany("INSERT INTO store VALUES (?, ?, ?)", items)
    connection.commit()


def view():
    cursor.execute("SELECT * FROM store")
    rows = cursor.fetchall()
    return rows


def delete(item):
    cursor.execute("DELETE FROM store WHERE item=?", (item,))
    connection.commit()


def update(quantity, price, item):
    cursor.execute(
        "UPDATE store SET quantity=?, price=? WHERE item=?", (quantity, price, item))
    connection.commit()


def get_formatted_products():
    products_list = view()
    productsTable = Table("Item", "Quantity", "Price")
    for item in products_list:
        productsTable.add_row(item[0], str(item[1]), str(item[2]))
    console.print(productsTable)


if __name__ == '__main__':
    get_formatted_products()
    connection.close()
