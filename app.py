import os
from flask_pymongo import PyMongo
from flask import Flask, flash, \
    render_template, redirect, request, session, url_for
from bson.objectid import ObjectId
from dotenv import load_dotenv
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
    """Render the home page.
    Returns: A rendered template for the index page."""
    return render_template('index.html')


@app.route('/about')
def about():
    """Render the about page.
    Returns: A rendered template for the about page."""
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login.
    On GET request, renders the login page.
    On POST request, verifies the user's credentials and logs them in.
    Returns:
    On successful login, redirects to the user's wardrobe page.
    On failure, reloads the login page with an error message."""
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one({
            "username": request.form.get("username").lower()})
        if existing_user:
            if check_password_hash(existing_user["password"],
                                   request.form.get("password")):
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
    """Log out the current user. Pops the user from the
    session and redirects to the home page.
    Returns: A redirect to the home page after logging out the user."""
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration.
    On GET request, renders the registration page.
    On POST request, registers a new user if the username is not already taken.
    Returns:
    On successful registration, redirects to the user's wardrobe page.
    On failure (e.g., username exists), reloads the
    registration page with an error message."""
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
    """Display and manage the user's wardrobe.
    On GET request, displays the user's wardrobe items
        or filters them based on a search query.
    On POST request, adds a new item to the user's wardrobe.
    Returns: A rendered template for the wardrobe page
    displaying the wardrobe items."""

    user_id = mongo.db.users.find_one({'username': session.get('user')})['_id']

    if request.method == 'POST':
        item_type = request.form['type']
        color = request.form['color']
        style = request.form['style']
        seasons = request.form.getlist('seasons')
        image_url = request.form['image_url']

        # Use a default image if no image URL is provided
        if not image_url:
            image_url = url_for('static', filename='images/no-image.png')

        # Insert the new item into the wardrobe collection
        mongo.db.wardrobe.insert_one({
            'user_id': ObjectId(user_id),
            'type': item_type,
            'color': color,
            'style': style,
            'seasons': seasons,
            'image_url': image_url
        })

        flash('Item added to your wardrobe!', 'success')
        return redirect(url_for('wardrobe'))

    search_query = request.args.get('search')
    if search_query:
        # Search for items that match the search query
        wardrobe_items = mongo.db.wardrobe.find({'user_id': user_id,
            "type": {"$regex": search_query, "$options": "i"}})
    else:
        # Retrieve the user's wardrobe items from the database
        wardrobe_items = mongo.db.wardrobe.find({'user_id': user_id})
    return render_template('wardrobe.html', wardrobe_items=wardrobe_items)


@app.route("/wardrobe/edit/<item_id>", methods=['GET', 'POST'])
def edit_item(item_id):
    """Edit an item in the user's wardrobe.
    On GET request, renders the edit item form with the current item details.
    On POST request, updates the item in the database with the new details.
    Only the owner of the item can edit it.
    Returns:
    On successful edit, redirects to the wardrobe page.
    On unauthorized access, redirects to the wardrobe page
    with an error message."""
    item = mongo.db.wardrobe.find_one({'_id': ObjectId(item_id)})

    user_id = mongo.db.users.find_one({'username': session.get('user')})['_id']
    if item['user_id'] != user_id:
        flash('You are not authorized to edit this item.', 'danger')
        return redirect(url_for('wardrobe'))

    if request.method == 'POST':
        seasons = request.form.getlist('seasons')

        # Check if an image URL was provided,
        # otherwise use a default or existing image
        image_url = request.form['image_url']
        if not image_url:
            image_url = url_for('static', filename='images/no-image.png')

        # Update the item in the database
        mongo.db.wardrobe.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': {
                'type': request.form['type'],
                'color': request.form['color'],
                'style': request.form['style'],
                'seasons': seasons,
                'image_url': image_url
            }}
        )
        flash('Item updated successfully!', 'success')
        return redirect(url_for('wardrobe'))

    return render_template('edit_item.html', item=item)


@app.route("/wardrobe/delete/<item_id>", methods=['POST'])
def delete_item(item_id):
    """Delete an item from the user's wardrobe.
    Returns: A redirect to the wardrobe page after successful deletion."""
    mongo.db.wardrobe.delete_one({'_id': ObjectId(item_id)})
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('wardrobe'))


@app.route('/outfit_suggestions', methods=['GET', 'POST'])
def outfit_suggestions():
    """Generate outfit suggestions based on the user's
    wardrobe, season, and occasion.
    On GET request, renders the form to select season and occasion.
    On POST request, generates and displays three outfit suggestions.
    Returns:
    A rendered template with outfit suggestions
    or the form to select criteria."""
    if request.method == 'POST':
        current_season = request.form['seasons']
        occasion = request.form['occasion']

        user_id = mongo.db.users.find_one(session.get('user_id'))['_id']

        wardrobe_items = mongo.db.wardrobe.find({
            'user_id': ObjectId(user_id),
            'seasons': {'$in': [current_season]},
            'style': occasion
        })
        tops = []
        bottoms = []
        dresses = []
        outerwear = []
        shoes = []
        accessories = []

        for item in wardrobe_items:
            if item['type'] == 'Top':
                tops.append(item)
            elif item['type'] == 'Bottom':
                bottoms.append(item)
            elif item['type'] == 'Dress':
                dresses.append(item)
            elif item['type'] == 'Outerwear':
                outerwear.append(item)
            elif item['type'] == 'Shoes':
                shoes.append(item)
            elif item['type'] == 'Accessory':
                accessories.append(item)

        from random import choice

        outfit_suggestions = []
        for _ in range(3):
            outfit = {}

            # Randomly decide to use either a dress or a top + bottom
            if dresses and choice([True, False]):
                outfit['dress'] = choice(dresses)
                outfit['top'] = None
                outfit['bottom'] = None
            else:
                outfit['top'] = choice(tops) if tops else None
                outfit['bottom'] = choice(bottoms) if bottoms else None
                outfit['dress'] = None

            outfit['outerwear'] = choice(outerwear) if outerwear else None
            outfit['shoes'] = choice(shoes) if shoes else None
            outfit['accessories'] = \
                choice(accessories) if accessories else None

            outfit_suggestions.append(outfit)

        return render_template('outfit_suggestions.html',
                               outfit_suggestions=outfit_suggestions)

    return render_template('outfit_form.html')


@app.route('/contact')
def contact():
    """Render the contact page.
    Returns: A rendered template for the contact page."""
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', IP),
        port=int(os.environ.get('PORT', PORT)),
        debug=False)
