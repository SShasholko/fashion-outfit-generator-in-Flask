import os
import pymongo
from flask_pymongo import PyMongo
from flask import Flask, flash, render_template, redirect, request, session, url_for
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

load_dotenv()

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
IP = os.getenv('IP')
PORT = os.getenv('PORT')
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.secret_key = os.getenv('SECRET_KEY')

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})
        if existing_user:
            if check_password_hash(existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(url_for("wardrobe", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template('login.html')

@app.route('/logout')
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for('wardrobe', username=session["user"]))
    return render_template('register.html')

@app.route('/wardrobe')
def wardrobe():
    # Handle displaying the user's wardrobe
    return render_template('wardrobe.html')

@app.route('/outfit_suggestions')
def outfit_suggestions():
    # Handle generating and displaying outfit suggestions
    return render_template('outfit_suggestions.html')




if __name__ == '__main__':
    app.run(
        host = os.environ.get('IP', IP),
        port = int(os.environ.get('PORT', PORT)),
        debug=True)