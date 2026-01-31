 from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
from werkzeug.security import generate_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
 
app = Flask(__name__)
app.secret_key = "civic_secret_key"

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qwe123",
    database="civic"
)
cursor = db.cursor(dictionary=True)
EMAIL_ADDRESS = "hemmanthguna@gmail.com"
EMAIL_PASSWORD = "zmiz tcqx ldnm oqzb"

# ---------------- LOGIN REQUIRED DECORATOR ----------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please login to continue", "error")
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function
@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')
@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form['email']

    cursor.execute(
        "SELECT email FROM user WHERE email=%s",
        (email,)
    )
    user = cursor.fetchone()

    if not user:
        flash("Email not registered", "error")
        return redirect(url_for('forgot_password'))

    # Generate temporary password
    temp_password = ''.join(
        random.choices(string.ascii_letters + string.digits, k=8)
    )

    hashed_password = generate_password_hash(temp_password)

    cursor.execute(
        "UPDATE user SET password=%s WHERE email=%s",
        (hashed_password, email)
    )
    db.commit()

    # SEND EMAIL (SECURE)
    send_email(email, temp_password)

    flash("Temporary password has been sent to your email", "success")
    return redirect(url_for('login_page'))


# ---------------- HOME (PUBLIC) ----------------
@app.route('/')
def home():
    return render_template('home.html')

# ---------------- SHOW LOGIN PAGE ----------------
@app.route('/login')
def login_page():
    return render_template('login.html')

# ---------------- LOGIN CHECK ----------------
@app.route('/login_check', methods=['POST'])
def login_check():
    email = request.form['email']
    password = request.form['password']

    # fetch user by email (PRIMARY KEY)
    cursor.execute(
        "SELECT * FROM user WHERE email=%s",
        (email,)
    )
    user = cursor.fetchone()

    if user and check_password_hash(user['password'], password):
        session['user'] = user['email']
        session['username'] = user['name']

        flash(f"Welcome, {user['name']} 👋", "welcome")
        return redirect(url_for('home'))
    else:
        flash("Invalid email or password", "error")
        return redirect(url_for('login_page'))

# ---------------- SHOW SIGNUP PAGE ----------------
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # ✅ CHECK IF EMAIL ALREADY EXISTS (email is PRIMARY KEY)
    cursor.execute(
        "SELECT email FROM user WHERE email=%s",
        (email,)
    )
    existing_user = cursor.fetchone()

    if existing_user:
        flash("Email already exists. Please login.", "error")
        return redirect(url_for('login_page'))

    # 🔐 HASH PASSWORD
    hashed_password = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)",
        (name, email, hashed_password)
    )
    db.commit()

    session['user'] = email
    session['username'] = name

    flash(f"Welcome, {name} 👋", "welcome")
    return redirect(url_for('home'))

# ---------------- ADD COMPLAINT (PROTECTED) ----------------
@app.route('/add_complaint')
@login_required
def add_complaint():
    return render_template('add_complaint.html')

# ---------------- VIEW COMPLAINTS (PROTECTED) ----------------
@app.route('/complaints')
@login_required
def complaints():
    return render_template('complaints.html')

# ---------------- PROFILE (PROTECTED) ----------------
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('login_page'))
def send_email(to_email, temp_password):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = "Civic App - Password Reset"

    body = f"""
Hello,

Your temporary password is:

{temp_password}

Please login using this password and change it immediately.

Regards,
Civic Issue Reporting Team
"""
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
