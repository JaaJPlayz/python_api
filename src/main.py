import sqlite3
from rich.console import Console
from rich.table import Table

console = Console()

connection = sqlite3.connect('./src/db/database.sqlite')

cursor = connection.cursor()


def create_table():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)")


def insert(item, quantity, price):
    cursor.execute("INSERT INTO store VALUES (?, ?, ?)",
                   (item, quantity, price))
    connection.commit()


def insert_from_input():
    item = input("Enter item: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))
    insert(item, quantity, price)


def insert_many(items):
    cursor.executemany("INSERT INTO store VALUES (?, ?, ?)", items)
    connection.commit()


def view():
    cursor.execute("SELECT * FROM store")
    rows = cursor.fetchall()
    return rows


def update(quantity, price, item):
    cursor.execute(
        "UPDATE store SET quantity=?, price=? WHERE item=?", (quantity, price, item))
    connection.commit()


def delete(item):
    cursor.execute("DELETE FROM store WHERE item=?", (item,))
    connection.commit()


def get_formatted_products():
    products_list = view()
    productsTable = Table("Item", "Quantity", "Price")
    for item in products_list:
        productsTable.add_row(item[0], str(item[1]), str(item[2]))
    console.print(productsTable)


def application_menu():
    options = ["Insert", "View", "Update", "Delete", "Exit"]
    while True:
        for index, option in enumerate(options):
            console.print(f"{index+1}. {option}")

        user_input = int(input("Choose an option: "))

        if user_input == 1:
            insert_from_input()

        elif user_input == 2:
            get_formatted_products()

        elif user_input == 3:
            item = input("Enter item to update: ")
            quantity = int(input("Enter new quantity: "))
            price = float(input("Enter new price: "))
            update(quantity, price, item)

        elif user_input == 4:
            item = input("Enter item to delete: ")
            delete(item)

        elif user_input == 5:
            break

        else:
            console.print("Invalid option", style="bold red")


if __name__ == '__main__':
    application_menu()
    connection.close()
