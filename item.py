class Item:
    """Class to represent Item entry in database"""

    def __init__(self, name, barcode, notes, bin_number):
        self.name = name
        self.barcode = barcode
        self.notes = notes
        self.bin = bin_number

    def __repr__(self):
        return f"""
                  Name: {self.name}
                  Barcode: {self.barcode}
                  Bin: {self.bin}
                  Notes: {self.notes}
                """
