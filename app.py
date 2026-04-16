from flask import *
from db_access import db_access
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

db = db_access()

app.secret_key = secrets.token_hex(16)

@app.route("/")
def default():
	return redirect(url_for("inventory"))
	
@app.route("/test")
def test():
	return "<h1>TEST</h1>"

@app.route("/login")
def login():
	username = "testing"
	return render_template("log-in.html", name=username)

@app.route("/login-submit", methods=["POST"])
def login_attempt():
	username = request.form.get("username")
	password = request.form.get("password")
	user = db.get_user_info(username)
	print(user)
	if user and check_password_hash(user[2], password): #successful login
		session['user'] = user[0] #user ID
		session['clearance'] = user[3]
		return redirect(url_for("inventory"))
	else: #failed login
		return redirect(url_for("login"))

@app.route("/create-user")
def create_user():
	return render_template("user-create.html")


@app.route("/create-user-submit", methods=["POST"])
def create_user_submit():
	username = request.form.get("username")
	password = request.form.get("password")
	clearance = request.form.get("clearance")
	hashed_pass = generate_password_hash(password)
	db.add_user(username, hashed_pass, clearance)
	return redirect(url_for("create_user"))

@app.route("/inventory")
def inventory():
	# connect to database, update html
	items = db.get_items()
	return render_template("inventory-page.html", items=items)

@app.route("/submit-item", methods=["POST"])
def submit():
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

@app.route("/images/<filename>")
def images(filename):
	return send_from_directory('images', filename)

if __name__ == "__main__":
    app.run(debug=True)