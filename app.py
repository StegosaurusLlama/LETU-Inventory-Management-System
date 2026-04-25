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
	
@app.route("/test")
def test():
	return "<h1>TEST</h1>"

@app.route("/login")
def login():
	username = "testing"
	return render_template("log-in.html", name=username)

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
	clearance = request.form.get("clearance")
	hashed_pass = generate_password_hash(password)
	db.add_user(username, hashed_pass, clearance)
	return redirect(url_for("user_account"))

@app.route("/change-password", methods=["POST"])
def change_password():
	db.change_password(session["userID"], generate_password_hash(request.form.get("password")))
	return redirect(url_for("user_account"))

@app.route("/inventory")
def inventory():
	# connect to database, update html
	search = request.args.get("search")
	if not search:
		search = ""
	rows = db.search_items(search)
	for r in rows:
		r["tags"] = db.get_product_tags(r["productID"])
		if not r["lowThreshhold"] or r["quantity"] > r["lowThreshhold"]:
			r["color"] = "#FFFFFF"
		elif r["quantity"] > 0:
			r["color"] = "#FFAA0C"
		else:
			r["color"] = "#E44242"	
			
	return render_template("inventory-page.html", items=rows, search=search)

@app.route("/submit-item", methods=["POST"])
def submit_item():
	name = request.form.get("name")
	price = request.form.get("price")
	amount = request.form.get("amount")
	desc = request.form.get("desc")
	lowCount = request.form.get("lowCount")
	imageFile = request.files['imageFile']
	imagePath = "images/" + name + Path(imageFile.filename).suffix
	imageFile.save(imagePath)
	db.add_item(name, price, amount, desc, lowCount, imagePath)
	return redirect(url_for("inventory"))

@app.route("/submit-tag", methods=["POST"])
def submit_tag():
	name = request.form.get("name")
	db.make_tag(name)
	productID = request.form.get("productID")
	row = db.get_tag_by_name(name)[0]
	db.apply_tag(productID, row["tagID"])
	if not name:
		return "FAIL"
	return redirect(url_for("inventory"))

@app.route("/images/<filename>")
def images(filename):
	return send_from_directory('images', filename)

@app.route("/submit-edit-item", methods=["POST"])
def edit_item():
	name = request.form.get("name")
	desc = request.form.get("description")
	productID = request.form.get("productID")
	db.edit_item(productID, name, desc)
	return redirect(url_for("inventory"))
    
@app.route("/remove-tag", methods=["POST"])
def remove_tag():
    productID = request.form.get("productID")
    tagID = request.form.get("tagID")
    db.remove_tag(productID, tagID)
    return redirect(url_for("inventory"))


@app.route("/submit-search", methods=["POST"])
def submit_search():
	search = request.form.get("search")
	return redirect(url_for("inventory")+"?search="+search)


if __name__ == "__main__":
    app.run(debug=True)