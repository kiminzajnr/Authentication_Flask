import os
from flask import (
    Flask,
    session,
    render_template,
    request,
    abort,
    flash,
    redirect,
    url_for,
)
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
# Secret key generated with secrets.token_urlsafe()
app.secret_key = "lkaQT-kAb6aIvqWETVcCQ28F-j-rP_PSEaCDdTynkXA"

# Use MongoDB to store users
users = {}

# Protect this endpont to be accessible to only logged users
# Tutorial https://blog.teclado.com/decorators-in-python/
@app.get("/")
def home():
    return render_template("home.html", email=session.get("email"))


# Protect this endpont to be accessible to only logged users
@app.get("/protected")
def protected():
    if not session.get("email"):
        abort(401, "User not authenticated")
    return render_template("protected.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if pbkdf2_sha256.verify(password, users.get(email)):
            session["email"] = email
            return redirect(url_for("protected"))
        abort(401, "incorrect Email or password")


    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        users[email] = pbkdf2_sha256.hash(password)
        print(users)
        flash("Signed up successfully.")
        return redirect(url_for("login"))

    return render_template("signup.html")