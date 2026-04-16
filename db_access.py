import sqlite3

class db_access:

    def __init__(self):
        pass
    
    def connect(self):
        conn = sqlite3.connect("Inventory_Data.sqlite3")
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def add_item(self, name, price, amount, desc, lowCount, imgurl):
        conn = self.connect()
        cursor = conn.cursor()
        print("INSERTING")
        cursor.execute("INSERT INTO stockitem (name, price, quantity, description, lowthreshhold, image) VALUES (?,?,?,?,?,?)", (name, price, amount, desc, lowCount, imgurl))
        conn.commit()
        conn.close()

    def get_items(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stockitem")
        rows = cursor.fetchall()
        conn.close()
        result = []
        for r in rows:
            result.append({"id": r[0], "name": r[1], "price": r[2], "desc": r[4], "imgurl": r[6]})
        return result
    
    def add_user(self, username, hashed_pass, clearance):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, passwordHash, clearance) VALUES (?,?,?)", (username, hashed_pass, clearance))
        conn.commit()
        conn.close()
        

    def get_user_info(self, username):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = (?)", (username,))
        user = cursor.fetchall()[0]
        conn.close()
        return user
