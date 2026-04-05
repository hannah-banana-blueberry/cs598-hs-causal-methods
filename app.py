from flask import Flask, render_template, url_for, request, redirect, session, jsonify, flash

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        return f"Hello, {username}!"
    return render_template("login.html")



@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        return f"Hello, {username}!"
    return render_template("home.html")

if __name__ == '__main__':
    # Parameter debug=True allows me to manually stop and restart
    #   server every time I edit the code
    app.run(debug=True)