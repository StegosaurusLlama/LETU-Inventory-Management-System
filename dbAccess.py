import sqlite3

class dbAccess:

    def __init__(self):
        pass
    
    
    def add_item(self):
        conn = sqlite3.connect("Inventory_Data.sqlite3")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO STOCKITEM VALUES (1, 'TestItem', 5.25, 8, 'This is a test', 3)")