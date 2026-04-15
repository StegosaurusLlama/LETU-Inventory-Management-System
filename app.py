from flask import *
from dbAccess import dbAccess

app = Flask(__name__)
db = dbAccess()
@app.route("/")
def hello_world():
	return "<a href='/login'><p>Hello, World!</p></a>"
	
@app.route("/test")
def test():
	return "<h1>TEST</h1>"

@app.route("/login")
def login():
	username = "testing"
	return render_template("log_in.html", name=username)

@app.route("/login-submit", methods=["POST"])
def login_attempt():
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
	return render_template("inventory page.html")

def getDatabase():
	pass