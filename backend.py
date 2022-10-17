"""
Provides backend for GUI Smart Bin App
"""

from datetime import datetime
import sqlite3
import json
import uuid
import boto3
#import RPi.GPIO as GPIO
from time import sleep
from config import (
    AWS_DYNAMODB_ENDPOINT,
    AWS_REGION,
    CREDENTIALS_FILE,
    OUTPUT_PINS,
    SQLITE_DB_LOCATION,
    SQLITE_INIT_FILE,
    TABLE_NAME,
)
from item import Item


class Backend:
    """Provides backend for GUI Smart Bin App"""

    # ============================ Private Methods ============================

    def __init__(self, gui):
        self.gui = gui

        # Setup Raspberry Pi Connection
        """ GPIO.setmode(GPIO.BCM)
        GPIO.setup(OUTPUT_PINS[0], GPIO.OUT)
        GPIO.setup(OUTPUT_PINS[1], GPIO.OUT)
        GPIO.setup(OUTPUT_PINS[2], GPIO.OUT)
        GPIO.setup(OUTPUT_PINS[3], GPIO.OUT) """

        # Setup SQLite database
        self.db_connection = sqlite3.connect(SQLITE_DB_LOCATION)
        self.__init_db(SQLITE_INIT_FILE)

        # Setup DynamoDB connection

        f = open(CREDENTIALS_FILE, encoding="UTF8")
        aws_creds = json.load(f)
        f.close()

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=AWS_REGION,
            #endpoint_url=AWS_DYNAMODB_ENDPOINT, Testing only
            aws_access_key_id=aws_creds["Access key ID"],
            aws_secret_access_key=aws_creds["Secret access key"],
        )
        self.__init_dynamodb()

    def __init_dynamodb(self):
        table_names = [table.name for table in self.dynamodb.tables.all()]

        if TABLE_NAME not in table_names:
            print("Creating DynamoDB table")
            self.dynamodb.create_table(
                TableName=TABLE_NAME,
                KeySchema=[{"AttributeName": "Id", "KeyType": "HASH"}],
                AttributeDefinitions=[
                    {"AttributeName": "Id", "AttributeType": "S"},
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1,
                },
            )
            print("DynamoDB table created")

    def __init_db(self, init_file):

        # Load JSON
        f = open(init_file, encoding="UTF8")
        item_data = json.load(f)
        f.close()

        cursor = self.db_connection.cursor()

        # Create table
        cursor.execute(
            """CREATE TABLE items (
                name text,
                barcode text,
                notes text,
                bin integer
            )"""
        )
        self.db_connection.commit()

        # Iterate over items in item_data, inserting each item
        for item in item_data["items"]:
            self.__insert_item(
                item["name"], item["barcode"], item["notes"], item["bin"]
            )

    def __del__(self):
        print("Cleaning up backend...")

        print("CURRENT DATABASE DATA:")
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM items")
        print(cursor.fetchall())

        self.db_connection.close()

    def __retrieve_item(self, item_input):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT * FROM items WHERE name LIKE '%{item_input.lower()}%' OR barcode='{item_input}'"
        )
        item = cursor.fetchone()

        if not item:
            return None

        return item

    def __insert_item(self, name="", barcode="", notes="", bin_number=-1):
        if bin_number == -1:
            raise Exception("Bin Number must be specified and within range 0-3")

        new_item = Item(
            name=name.lower(),
            barcode=barcode,
            notes=notes,
            bin_number=bin_number,
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
    
    def __log_disposal(self, name, bin_number):
         table = self.dynamodb.Table(TABLE_NAME)
         
         table.put_item(Item={
             "Id": str(uuid.uuid4()),
             "Time": datetime.utcnow().isoformat(),
             "Name": name,
             "BinNumber": bin_number
         })

    def highlight_bin(self, bin_number):
        if bin_number == 0:
            GPIO.output(OUTPUT_PINS[0], GPIO.HIGH)
            sleep(5)
            GPIO.output(OUTPUT_PINS[0], GPIO.LOW)
        elif bin_number == 1:
            GPIO.output(OUTPUT_PINS[1], GPIO.HIGH)
            sleep(5)
            GPIO.output(OUTPUT_PINS[1], GPIO.LOW)
        elif bin_number == 2:
            GPIO.output(OUTPUT_PINS[2], GPIO.HIGH)
            sleep(5)
            GPIO.output(OUTPUT_PINS[2], GPIO.LOW)
        elif bin_number == 3:
            GPIO.output(OUTPUT_PINS[3], GPIO.HIGH)
            sleep(5)
            GPIO.output(OUTPUT_PINS[3], GPIO.LOW)
        else:
            print(f'Error highlighting bin: Bin number "{bin_number}" does not exist.')

    def __clear_input(self):
        self.gui.input_box.delete(0, 'end')
    # ============================ Public Methods =============================

    def process_item(self):
        # Fetch text entry from input
        item_input = self.gui.input_text.get()
        item = self.__retrieve_item(item_input)
        if not item:
            print(f"Item corresponding to {item_input} does not exist")
            return

        self.__log_disposal(item[0], item[3])
        self.__clear_input()
