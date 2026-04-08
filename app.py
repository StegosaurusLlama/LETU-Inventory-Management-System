from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
	return "<a href='/test'><p>Hello, World!</p></a>"
	
@app.route("/test")
def test():
	return "<h1>TEST</h1>"
	
def getDatabase():
	pass