from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secretkey"

# =========================
# MYSQL CONNECTION
# =========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qwe123",   # YOUR MYSQL PASSWORD
    database="civic"
)
cursor = db.cursor()

# =========================
# ROUTES
# =========================
@app.route("/")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

# =========================
# REGISTER (NO PHOTO)
# =========================
@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    password = generate_password_hash(request.form["password"])

    cursor.execute("SELECT email FROM user WHERE email=%s", (email,))
    if cursor.fetchone():
        flash("Email already registered!", "error")
        return redirect(url_for("signup"))

    cursor.execute(
        "INSERT INTO user (name, email, password, profile_photo) VALUES (%s, %s, %s, %s)",
        (name, email, password, None)
    )
    db.commit()

    flash("Signup successful! Please login.", "success")
    return redirect(url_for("login"))

# =========================
# LOGIN CHECK
# =========================
@app.route("/login_check", methods=["POST"])
def login_check():
    email = request.form["email"]
    password = request.form["password"]

    cursor.execute("SELECT password FROM user WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user:
        if check_password_hash(user[0], password):
            flash("Login successful!", "success")
            return redirect(url_for("login"))
        else:
            flash("Incorrect password!", "error")
            return redirect(url_for("login"))
    else:
        flash("User not found!", "error")
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
