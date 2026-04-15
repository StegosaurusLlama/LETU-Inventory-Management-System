from flask import *
from dbAccess import dbAccess

app = Flask(__name__)
db = dbAccess()
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
def loginAttempt():
	name = request.form.get("username")
	print(name)
	if name == "admin":
		db.add_item()
		return "<h1>Hello Admin</h1>"
	elif name == "inventory":
		return redirect(url_for("inventory"))
	else:
		return redirect(url_for("login"))

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