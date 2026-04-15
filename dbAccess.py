import sqlite3

class dbAccess:

    temp = 0
    def __init__(self):
        pass
    
    
    def add_item(self):
        conn = sqlite3.connect("Inventory_Data.sqlite3")
        cursor = conn.cursor()
        print("INSERTING")
        cursor.execute("INSERT INTO stockitem (name, price, quantity, description, lowthreshhold) VALUES (?,?,?,?,?)", ('TestItem'+str(self.temp), 5.25, 8, 'This is a test', 3))
        self.temp += 1
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
            print(r)
            result.append({"num": r[0], "name": r[1], "price": r[2], "desc": r[4]})
        return result