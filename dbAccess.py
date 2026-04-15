import sqlite3

class dbAccess:

    def __init__(self):
        pass
    
    
    def add_item(self, name, price, amount, desc, lowCount, imgurl):
        conn = sqlite3.connect("Inventory_Data.sqlite3")
        cursor = conn.cursor()
        print("INSERTING")
        cursor.execute("INSERT INTO stockitem (name, price, quantity, description, lowthreshhold, image) VALUES (?,?,?,?,?,?)", (name, price, amount, desc, lowCount, imgurl))
        conn.commit()
        conn.close()

    def get_items(self):
        conn = sqlite3.connect("Inventory_Data.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stockitem")
        rows = cursor.fetchall()
        conn.close()
        result = []
        for r in rows:
            result.append({"id": r[0], "name": r[1], "price": r[2], "desc": r[4], "imgurl": r[6]})
        return result