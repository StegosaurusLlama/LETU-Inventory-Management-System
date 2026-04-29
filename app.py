from flask import *
from db_access import db_access
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path

app = Flask(__name__)

db = db_access()

app.secret_key = secrets.token_hex(16)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True, 
    SESSION_COOKIE_SAMESITE='Strict' 
)


@app.before_request
def check_session():
	if "clearance" not in session and request.endpoint not in ["login", "login_attempt"]:
		return redirect(url_for("login"))

@app.route("/")
def default():
	return redirect(url_for("login"))

@app.route("/login")
def login():
	return render_template("log-in.html")

@app.route("/log-out", methods=["POST"])
def log_out():
	session.clear()
	return redirect(url_for("login"))

@app.route("/login-submit", methods=["POST"])
def login_attempt():
	username = request.form.get("username")
	password = request.form.get("password")
	users = db.get_user_info(username)
	if not users: #failed login
		return redirect(url_for("login"))
	user = users[0]
	if check_password_hash(user["passwordHash"], password): #successful login
		session["userID"] = user["userID"] #user ID
		session["username"] = user["username"] #user ID
		session["clearance"] = user["clearance"]
		return redirect(url_for("inventory"))
	else: #failed login
		return redirect(url_for("login"))

@app.route("/user-accounts")
def user_account():
	return render_template("user-accounts.html")

@app.route("/create-user-submit", methods=["POST"])
def create_user_submit():
	username = request.form.get("username")
	password = request.form.get("password")
	confirm = request.form.get("confirm")
	clearance = request.form.get("clearance")
	hashed_pass = generate_password_hash(password)
	if password==confirm:
		db.add_user(session["userID"], username, hashed_pass, clearance)
		return redirect(url_for("user_account"))
	else:
		return redirect(url_for("user_account"))

@app.route("/edit-user-submit", methods=["POST"])
def edit_user_submit():
	username = request.form.get("username")
	user_ID = db.get_user_info(username)[0]["userID"]
	password = request.form.get("password")
	confirm = request.form.get("confirm")
	if password==confirm:
		db.change_password(session["userID"], user_ID, username, generate_password_hash(password))
		return redirect(url_for("user_account"))
	else:
		return redirect(url_for("user_account"))

@app.route("/delete-user-account", methods=["POST"])
def delete_user_account():
    username = request.form.get("username")
    confirm = request.form.get("confirm")
    user_ID = db.get_user_info(username)[0]["userID"]
    if username==confirm:
        db.delete_user(session["userID"], user_ID, username)
        return redirect(url_for("user_account"))
    else:
        return redirect(url_for("user_account"))
    

@app.route("/change-password", methods=["POST"])
def change_password():
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    if password==confirm:
        db.change_password(session["userID"], session["userID"], generate_password_hash(password))
        return redirect(url_for("user_account"))
    else:
        return redirect(url_for("user_accounts"))

@app.route("/inventory")
def inventory():
	# connect to database, update html
	search = request.args.get("search")
	search_tags = request.args.getlist("tags")
	if not search:
		search = ""
	if not search_tags:
		search_tags = []
	print(search_tags)
	rows = db.search_items(search, search_tags)
	tags = db.get_tags()
	if not rows:
		rows = []
	for r in rows:
		r["tags"] = db.get_product_tags(r["productID"])
		if not r["lowThreshhold"] or r["quantity"] > r["lowThreshhold"]:
			r["color"] = "#FFFFFF"
		elif r["quantity"] > 0:
			r["color"] = "#FFAA0C"
		else:
			r["color"] = "#E44242"	
			
	return render_template("inventory-page.html", items=rows, search=search, searchTags=search_tags, tags=tags)

@app.route("/submit-item", methods=["POST"])
def submit_item():
	name = request.form.get("name")
	price = request.form.get("price")
	amount = request.form.get("amount")
	quantity = request.form.get("quantity")
	desc = request.form.get("desc")
	lowCount = request.form.get("lowCount")
	imageFile = request.files['imageFile']
	imagePath = "images/" + name + Path(imageFile.filename).suffix
	imageFile.save(imagePath)
	db.add_item(session["userID"], name, price, amount, desc, lowCount, imagePath)
	return redirect(url_for("inventory"))

@app.route("/submit-edit-stock", methods=["POST"])
def submit_stock():
	stock = int(request.form.get("quantity"))
	productID = request.form.get("productID")
	lowThreshhold = int(request.form.get("lowThreshhold"))
	
	if stock == 0:
		stocked = 0
	elif stock <= lowThreshhold:
		stocked = 1
	else:
		stocked = 2
	db.edit_item_stock(session["userID"], productID, stock)
	return jsonify({"productID": productID, "stocked": stocked})

@app.route("/create-tag", methods=["POST"])
def create_tag():
	name = request.form.get("name") or ""
	db.make_tag(session["userID"], name)
	productID = request.form.get("productID")
	row = db.get_tag_by_name(name)[0]
	db.apply_tag(session["userID"], productID, row["tagID"])
	return redirect(url_for("inventory"))

@app.route("/delete-tag", methods=["POST"])
def delete_tag():
	name = request.form.get("name") or ""
	db.delete_tag(session["userID"], name)
	return redirect(url_for("inventory"))

@app.route("/submit-tags", methods=["POST"])
def submit_tag():
	tags = request.form.getlist("tags") or []
	productID = request.form.get("productID")
	for tagID in tags:
		db.apply_tag(session["userID"], productID, tagID)
	return redirect(url_for("inventory"))

@app.route("/images/<filename>")
def images(filename):
	return send_from_directory('images', filename)

@app.route("/submit-edit-item", methods=["POST"])
def edit_item():
	name = request.form.get("name")
	desc = request.form.get("description")
	productID = request.form.get("productID")
	price = request.form.get("price")
	quantity = request.form.get("quantity")
	db.edit_item(session["userID"], productID, name, desc, price, quantity)
	return jsonify({"productID":productID, "name":name, "desc":desc, "price":price, "quantity":quantity})
    
@app.route("/remove-tag", methods=["POST"])
def remove_tag():
    productID = request.form.get("productID")
    tagID = request.form.get("tagID")
    db.remove_tag(session["userID"], productID, tagID)
    return redirect(url_for("inventory"))


@app.route("/submit-search", methods=["POST"])
def submit_search():
	search = request.form.get("search")
	tags = request.form.getlist("tags")
	url = url_for("inventory")+"?search="+search
	for tag in tags:
		url += "&tags=" + tag
	return redirect(url)

@app.route("/audit-log")
def audit_log():
    logs = db.get_logs()
    return render_template("audit-log.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)