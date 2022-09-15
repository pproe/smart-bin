"""
Provides backend for GUI Smart Bin App
"""

import sqlite3
from item import Item


class Backend:
    """Provides backend for GUI Smart Bin App"""

    def __init__(self, gui, dblocation=":memory:"):
        self.gui = gui

        # Setup SQLite database
        self.db_connection = sqlite3.connect(dblocation)
        self.__init_db()

    def __init_db(self):
        cursor = self.db_connection.cursor()
        cursor.execute(
            """CREATE TABLE items (
                name text,
                barcode text,
                notes text,
                bin integer
            )"""
        )
        self.db_connection.commit()

    def __del__(self):
        print("Cleaning up backend...")

        print("CURRENT DATABASE DATA:")
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM items")
        print(cursor.fetchall())

        self.db_connection.close()

    def process_item(self):

        # Fetch text entry from input
        item_input = self.gui.input_text.get()
        self.insert_item(name=item_input, bin_number=1)

    def retrieve_bin_number(self, item_input):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT * FROM items WHERE name='{item_input}' OR barcode='{item_input}'"
        )
        return cursor.fetchone()

    def insert_item(self, name="", barcode="", notes="", bin_number=-1):
        if bin_number == -1:
            raise Exception("Bin Number must be specified and within range 0-3")

        new_item = Item(
            name=name, barcode=barcode, notes=notes, bin_number=bin_number
        )
        cursor = self.db_connection.cursor()
        cursor.execute(
            "INSERT INTO items VALUES (:name, :barcode, :notes, :bin)",
            {
                "name": new_item.name,
                "barcode": new_item.barcode,
                "notes": new_item.notes,
                "bin": new_item.bin,
            },
        )
        self.db_connection.commit()
