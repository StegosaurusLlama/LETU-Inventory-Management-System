import sqlite3
from datetime import datetime

class db_access:

    def __init__(self):
        pass
    
    def _connect(self):
        conn = sqlite3.connect("Inventory_Data.sqlite3")
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def _edit_data(self, userID, action, affected, query, args=(), num=0):
        username = self.get_userID_info(userID)[0]["username"]
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, args)
                auditQuery = "INSERT INTO InventoryChange (changeTime, userID, actionTaken, effectiveChange, changeQuantity) VALUES (?,?,?,?,?)"
                auditArgs = (datetime.now().strftime("%m-%d-%Y %H:%M:%S"), f"{username} (User #{userID})", action, affected, num)  
                cursor.execute(auditQuery, auditArgs)
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
    
    def add_item(self, userID, name, price, amount, desc, lowCount, imgurl):
        query = "INSERT INTO StockItem (name, price, quantity, description, lowThreshhold, image) VALUES (?,?,?,?,?,?)"
        args = (name, price, amount, desc, lowCount, imgurl)
        return self._edit_data(userID, "Created item", name, query, args)

    def get_items(self):
        query = "SELECT * FROM StockItem"
        return self._get_data(query)
    
    def edit_item(self, userID, productID, name, desc, price, quantity):
        query = "UPDATE StockItem SET name = ?, description = ?, price = ?, quantity = ? WHERE productID = ?"
        args = (name, desc, price, quantity, productID)
        return self._edit_data(userID, "Changed item", name, query, args)
    
    def edit_item_stock(self, userID, productID, name, quantity):
        query = "UPDATE StockItem SET quantity = ? WHERE productID = ?"
        args = (quantity, productID)
        return self._edit_data(userID, "Changed stock", name, query, args, quantity)
    
    # def edit_item_name(self, product_id, name):
    #     query = "UPDATE StockItem SET name = ? WHERE productID = ?"
    #     args = (name, product_id)
    #     return self._edit_data(query, args)
    
    # def edit_item_desc(self, product_id, desc):
    #     query = "UPDATE StockItem SET description = ? WHERE productID = ?"
    #     args = (desc, product_id)
    #     return self._edit_data(query, args)

    def add_user(self, userID, username, hashed_pass, clearance):
        query = "INSERT INTO Users (username, passwordHash, clearance) VALUES (?,?,?)"
        args = (username, hashed_pass, clearance)
        return self._edit_data(userID, "Created user", username, query, args)

    def get_user_info(self, username):
        query = "SELECT * FROM Users WHERE username = ?"
        args = (username,)
        return self._get_data(query, args)
    
    def get_userID_info(self, userID):
        query = "SELECT * FROM Users WHERE userID = ?"
        args = (userID,)
        return self._get_data(query, args)

    def change_password(self, userID, targetUserID, targetUsername, new_password):
        query = "UPDATE Users SET passwordHash = ? WHERE userID = ?"
        args = (new_password, targetUserID)
        return self._edit_data(userID, "Changed password", targetUsername, query, args)
    
    def delete_user(self, userID, targetUserID, targetUsername):
        query = "DELETE FROM Users WHERE userID = ?"
        args = (targetUserID,)
        return self._edit_data(userID, "Deleted User", targetUsername, query, args)
    
    def make_tag(self, userID, tagname):
        query = "INSERT INTO Tag (name) VALUES (?)"
        args = (tagname,)
        return self._edit_data(userID, "Created tag", tagname, query, args)

    def delete_tag(self, userID, tagname):
        query = "DELETE FROM Tag WHERE name = ?"
        args = (tagname,)
        return self._edit_data(userID, "Deleted tag", tagname, query, args)
    
    def apply_tag(self, userID, productID, tagID, productName, tagName):
        query = "INSERT INTO ProductTag (productID, tagID) VALUES (?,?)"
        args = (productID, tagID)
        return self._edit_data(userID, f"Applied tag {tagName}", productName, query, args)
    
    def remove_tag(self, userID, productID, tagID, productName, tagName):
        query = "DELETE FROM ProductTag WHERE productID = ? AND tagID = ?"
        args = (productID, tagID)
        return self._edit_data(userID, f"Removed tag {tagName}", productName, query, args)
    
    def get_items_with_tag(self, tagID):
        query = "SELECT S.* FROM ProductTag P INNER JOIN StockItem S ON P.productID = S.productID WHERE P.tagID = ?"
        args = (tagID,)
        return self._get_data(query, args)
    
    def get_product_tags(self, productID):
        query = "SELECT T.* FROM ProductTag P INNER JOIN Tag T ON P.tagID = T.tagID WHERE P.productID = ?"
        args = (productID,)
        return self._get_data(query, args)
    
    def get_tags(self):
        query= "SELECT * FROM Tag"
        return self._get_data(query)
    
    def get_tag_by_name(self, name):
        query = "SELECT * FROM Tag WHERE name = ?"
        args = (name,)
        return self._get_data(query, args)
    
    def search_items(self, search, tags=[]):
        query = f"SELECT DISTINCT S.*, (S.name LIKE ?) AS match_score, (S.name LIKE ?) AS match_begin FROM StockItem S {"INNER JOIN ProductTag P ON S.productID = P.productID" if tags else ""} {f"WHERE P.tagID IN ({','.join(['?'] * len(tags))})" if tags else ""} ORDER BY match_begin DESC, match_score DESC, S.name COLLATE NOCASE ASC"
        args = (f"%{search}%", f"{search}%") + tuple(tags)
        return self._get_data(query, args)
    
    def get_logs(self):
        query = "SELECT * FROM InventoryChange ORDER BY changeTime DESC"
        return self._get_data(query)