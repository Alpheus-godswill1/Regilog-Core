from flask import Flask, request, render_template, flash,  jsonify, redirect, url_for
from werkzeug.security import generate_password_hash
from config.db import get_db_connection
from utils.logger import setup_logger, logger
import os

setup_logger()
app = Flask(__name__)
app.config['SECRET_KEY'] =  os.getenv("SECRET_KEY", "this_secret_key_must_never_be_used")

@app.route("/")
def register():
    return render_template("register.html")
    logger.info("Rendering register.html template")

@app.route("/success/")
def success():
    username = request.args.get("username")
    return render_template("success.html", username=username)

@app.route("/registration/", methods=["GET", "POST"])
def registration():
    password_length = 8
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        errors = []
        if not username:
            errors.append("Username is required.")
        if not email:
            errors.append("Email is required.")
        if not password or len(password) < password_length:
            errors.append(f"Password is required and must be at least {password_length} characters long.")
        
        if errors:
            logger.warning(f"Registration failed for email {email}: {'==='.join(errors)}")
            for e in errors:
                flash(e, "error")
            return render_template("register.html", username=username,  email=email)

        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            con.close()
            flash("Email is already registered.", "error")
            logger.warning(f"Registration attempt with existing email: {email}")
            return render_template("register.html", username=username, email=email)
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))
        con.commit()
        con.close()

        logger.info(f"New user registered: {username} ({email})")
        flash("Registration successful!", "success")
        return redirect(url_for("success", username=username))

    return render_template("register.html", username=username)
    logger.info(f"User {username} registered successfully with email {email}")
if __name__ == "__main__":
    app.run(port=3000, debug=True, use_debugger=True)
