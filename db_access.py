import sqlite3

class db_access:

    def __init__(self):
        pass
    
    def _connect(self):
        conn = sqlite3.connect("Inventory_Data.sqlite3")
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def _edit_data(self, query, args=()):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, args)
            return True
        except Exception as e:
            print(e)
            return False

    
    def _get_data(self, query, args=()):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, args)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            print(e)
            return None
    
    def add_item(self, name, price, amount, desc, lowCount, imgurl):
        query = "INSERT INTO StockItem (name, price, quantity, description, lowThreshhold, image) VALUES (?,?,?,?,?,?)"
        args = (name, price, amount, desc, lowCount, imgurl)
        return self._edit_data(query, args)

    def get_items(self):
        query = "SELECT * FROM StockItem"
        print(self._get_data(query))
        return self._get_data(query)

    def add_user(self, username, hashed_pass, clearance):
        query = "INSERT INTO Users (username, passwordHash, clearance) VALUES (?,?,?)"
        args = (username, hashed_pass, clearance)
       
        return self._edit_data(query, args)

    def get_user_info(self, username):
        query = "SELECT * FROM Users WHERE username = ?"
        args = (username,)
        return self._get_data(query, args)
    
    def make_tag(self, tagname):
        query = "INSERT INTO Tag (name) VALUES (?)"
        args = (tagname,)
        return self._edit_data(query, args)

    def delete_tag(self, tagID):
        query = "DELETE FROM Tag WHERE tagID = ?"
        args = (tagID,)
        return self._edit_data(query, args)
    
    def apply_tag(self, productID, tagID):
        query = "INSERT INTO ProductTag (productID, tagID) VALUES (?,?)"
        args = (productID, tagID)
        return self._edit_data(query, args)
    
    def remove_tag(self, productID, tagID):
        query = "DELETE FROM ProductTag WHERE productID = ? AND tagID = ?"
        args = (productID, tagID)
        return self._edit_data(query, args)
    
    def get_items_with_tag(self, tagID):
        query = "SELECT S.* FROM ProductTag P INNER JOIN StockItem S ON P.productID = S.productID WHERE P.tagID = ?"
        args = (tagID,)
        return self._get_data(query, args)
    
    def get_tags(self, productID):
        query = "SELECT T.* FROM ProductTag P INNER JOIN Tag T ON P.tagID = T.tagID WHERE P.productID = ?"
        args = (productID,)
        print( self._get_data(query, args))
        return self._get_data(query, args)