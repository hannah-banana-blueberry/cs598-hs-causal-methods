from flask import Flask, render_template, url_for, request, redirect, session, jsonify, flash
from models import db, User, Excerpt

app = Flask(__name__)


# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev"

db.init_app(app)

# --------------------------
@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]

        user = User(username=username, password="test")
        db.session.add(user)
        db.session.commit()

        return f"Hello, {username}!"
    return render_template("login.html")



@app.route("/home", methods=["GET", "POST"])
def home():
    excerpt = Excerpt.query.first()

    parsed_excerpt = excerpt.from_db()

    return render_template(
        "reading_room.html",
        excerpt=excerpt,
        content=parsed_excerpt["excerpt_json"]
    )





if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    # Parameter debug=True allows me to automatically stop and restart
    #   server every time I edit the code (not manual)
    app.run(debug=True)