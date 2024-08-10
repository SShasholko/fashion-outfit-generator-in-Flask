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

@app.route('/wardrobe', methods=["GET", "POST"])
def wardrobe():
    # user_name = mongo.db.users.find_one(session.get('user_id'))['_id']
    # print(user_name)
    user_id = mongo.db.users.find_one(session.get('user_id'))['_id']
    if request.method == 'POST':
        # Handle form submission
        item_type = request.form['type']
        color = request.form['color']
        style = request.form['style']
        seasons = request.form.getlist('seasons')
        image_url = request.form['image_url']

        # Insert the new item into the wardrobe collection
        mongo.db.wardrobe.insert_one({
            'user_id': ObjectId(user_id),  # Replace with the actual user ID from your session
            'type': item_type,
            'color': color,
            'style': style,
            'seasons': seasons,
            'image_url': image_url
        })

        flash('Item added to your wardrobe!', 'success')
        return redirect(url_for('wardrobe'))

    # Retrieve the user's wardrobe items from the database
    wardrobe_items = mongo.db.wardrobe.find({'user_id': user_id})
    return render_template('wardrobe.html', wardrobe_items=wardrobe_items)

@app.route("/wardrobe/edit/<item_id>", methods=['GET', 'POST'])
def edit_item(item_id):
    item = mongo.db.wardrobe.find_one({'_id': ObjectId(item_id)})

    if request.method == 'POST':
        # Update the item in the database
        mongo.db.wardrobe.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': {
                'type': request.form['type'],
                'color': request.form['color'],
                'style': request.form['style'],
                'weather': request.form['weather'],
                'image_url': request.form['image_url']
            }}
        )
        flash('Item updated successfully!', 'success')
        return redirect(url_for('wardrobe'))

    return render_template('edit_item.html', item=item)

@app.route("/wardrobe/delete/<item_id>", methods=['POST'])
def delete_item(item_id):
    mongo.db.wardrobe.delete_one({'_id': ObjectId(item_id)})
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('wardrobe'))

    






@app.route('/outfit_suggestions')
def outfit_suggestions():
    # Handle generating and displaying outfit suggestions
    return render_template('outfit_suggestions.html')




if __name__ == '__main__':
    app.run(
        host = os.environ.get('IP', IP),
        port = int(os.environ.get('PORT', PORT)),
        debug=True)