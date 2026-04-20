from flask import *
from db_access import db_access
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

db = db_access()

app.secret_key = secrets.token_hex(16)

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

@app.route("/inventory")
def inventory():
	# connect to database, update html
	rows = db.get_items()
	for r in rows:
		r["tags"] = db.get_tags(r["productID"])
	return render_template("inventory-page.html", items=rows)

@app.route("/submit-item", methods=["POST"])
def submit_item():
	name = request.form.get("name")
	price = request.form.get("price")
	amount = request.form.get("amount")
	desc = request.form.get("desc")
	lowCount = request.form.get("lowCount")
	imageFile = request.files['imageFile']
	imagePath = "images/" + imageFile.filename
	imageFile.save(imagePath)
	db.add_item(name, price, amount, desc, lowCount, imagePath)
	return redirect(url_for("inventory"))

@app.route("/submit-tag", methods=["POST"])
def submit_tag():
	name = request.form.get("name")
	db.make_tag(name)
	productID = request.form.get("productID")
	print(productID)
	row = db._get_data("SELECT tagID FROM Tag WHERE name = ?", (name,))[0]
	print(row["tagID"])
	db.apply_tag(productID, row["tagID"])
	return redirect(url_for("inventory"))

@app.route("/images/<filename>")
def images(filename):
	return send_from_directory('images', filename)

if __name__ == "__main__":
    app.run(debug=True)