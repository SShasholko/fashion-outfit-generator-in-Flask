![Fashion Outfit Generator](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/mockup.png)

# Fashion Outfit Generator
## Introduction
Welcome to the Fashion Outfit Generator, your personal stylist right at your fingertips! 
### What It Does
The Fashion Outfit Generator is a web application that acts as your personal stylist. It allows you to digitize your wardrobe by adding items that you already own. Once your wardrobe is set up, the app generates outfit suggestions based on the season and the occasion. Key features include:

- **Digital Wardrobe**: Add and manage items from your real-life wardrobe.
- **Outfit Suggestions**: Receive tailored outfit recommendations for various occasions and weather conditions.
- **Search Functionality**: Easily find specific items in your wardrobe.
- **Wardrobe Management**: Edit and update your wardrobe items as needed.
- **User-Friendly Interface**: Enjoy a sleek design that makes fashion management a breeze.

### Why You'll Love It
In today's fast-paced world, deciding what to wear can be a time-consuming and often overwhelming task. Whether you're preparing for a special event, a casual outing, or just your everyday routine, choosing the right outfit is important, but it shouldn't be stressful. The Fashion Outfit Generator was created to simplify this process, helping you effortlessly coordinate your wardrobe to suit any occasion and weather. It's a tool for anyone who wants to make getting dressed easier and more enjoyable.

### Who It's For
The Fashion Outfit Generator is perfect for anyone who wants to streamline their fashion choices. Whether you're a fashion enthusiast looking to experiment with different styles or someone who prefers a more practical approach to getting dressed, this app is designed for you. It’s ideal for busy professionals, students, or anyone who wants to look their best without spending too much time deciding what to wear.

## ✨ Features
### 1. Home Page
![Home Page](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/Home+Page.png)
The Home Page welcomes users with a clean and stylish design.
#### Key Features:
- Hero Section with welcoming message and stylish background.
- Call to Action buttons for Login and Register.
- Responsive Design for all devices.

### 2. User Registration & Authentication
|Registration |  Authentication |
|--|--|
|  ![Registration](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/Registration.png)|  ![Authentication](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/Authentication.png)|

#### Explanation:
- **User Registration**: New users can create an account by providing a username, email, and password. The password is securely hashed using generate_password_hash before being stored in the database.

    **Example Code**:
```bash
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
```

- **User Login**: Users can log in using their registered credentials. If the username and password match, the user is redirected to their personalized wardrobe page.

    **Example Code**:
```bash
@app.route('/login', methods=['GET', 'POST'])
def login():
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
```

### 3. Personalized Wardrobe Management
![Wardrobe](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/Wardrobe.png)

#### Explanation:
- **Add New Item**: Users can add items to their wardrobe by specifying the type, color, style, and seasons for which the item is suitable. If no image URL is provided, a default image is used.
![Add New Item](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/Add+New+Items.png)

    **Example Code**:
```bash
if not image_url:
    image_url = url_for('static', filename='images/no-image.png')
```

- **Search Functionality**: Users can search their wardrobe by type, such as "dress" or "shoes." If the search field is empty, all wardrobe items are displayed.
![Search](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/search.png)

    **Example Code**:
```bash
    search_query = request.args.get('search')
    if search_query:
        wardrobe_items = mongo.db.wardrobe.find({'user_id': user_id, "type": {"$regex": search_query, "$options": "i"}})
    else:
        wardrobe_items = mongo.db.wardrobe.find({'user_id': user_id})
    return render_template('wardrobe.html', wardrobe_items=wardrobe_items)
```

- **Edit & Delete Items**: Users can edit or delete items from their wardrobe. Editing includes updating the type, color, style, seasons, and image. Deleting an item permanently removes it from the wardrobe.

|Edit Items |  Delete Items |
|--|--|
|  ![Edit](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/edit.png)| ![Delete Items](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/delete.png)|

### 4. Outfit Generation Based on Weather and Occasion
![Generation](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/generation.png)
![Suggestions](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/suggestions.png)

The Outfit Generation feature intelligently suggests outfits tailored to the current weather and the occasion you select. 

#### Explanation:

- **User Input**: The user selects the current weather (e.g., Spring, Summer, Autumn, Winter) and the type of occasion (e.g., Casual, Formal, Sporty).
- **Smart Matching**: The app cross-references the user’s wardrobe with the selected weather and occasion. It identifies items that are suitable for the given season and matches them with the occasion type.
- **Outfit Composition**: The app randomly combines wardrobe items such as tops, bottoms, dresses, outerwear, shoes, and accessories to create complete outfits. It ensures that each suggested outfit is cohesive and appropriate for the context.
- **Three Suggestions**: Users are presented with three distinct outfit options, providing a variety of choices to suit their style and preferences.

    **Example Code**:
```bash
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
```

### 5. Contact Us and About Page

| Contact Us |  About Pages |
|--|--|
|  ![Contact Us](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/contact+us.png)| ![About Page](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/about+page.png)|

#### Explanation:
- **About Page**: Provides a comprehensive overview of how the Fashion Outfit Generator works. It guides users through the process of adding clothing items to their virtual wardrobe and explains how to use the Outfit Generator to create tailored outfit suggestions based on weather conditions and specific occasions.

- **Contact Us Page**: Users can contact the developer via email or Facebook. This ensures that users can easily reach out for support or feedback.


### 6. Responsive Design and User-Friendly Interface
![Responsive Design](static/images/responsive.gif)

#### Explanation:
- The Fashion Outfit Generator is built with a responsive design using Bootstrap, ensuring that it looks great on all devices, whether it's a desktop, tablet, or mobile phone.

- The interface is intuitive, making it easy for users to navigate through the various features, from managing their wardrobe to generating outfits.

### 7. Security Features
**User Authentication and Authorization**:
The Fashion Outfit Generator ensures that user accounts are secure through robust authentication methods. Users must log in with a username and password, and passwords are hashed using secure hashing algorithms (bcrypt) before being stored in the database. This protects user credentials from being exposed in the event of a data breach.

  **Example Code**:
```bash
    "password": generate_password_hash(request.form.get("password"))
```

**Authorization Checks for Sensitive Operations**:
Certain actions, such as editing wardrobe items, require authorization to ensure that only the owner of the items or an authorized user can perform these operations. Each time an item is modified, the app verifies that the requesting user has the right permissions to carry out the action.

  **Example Code**:
```bash
    user_id = mongo.db.users.find_one({'username': session.get('user')})['_id']
    if item['user_id'] != user_id:
        flash('You are not authorized to edit this item.', 'danger')
        return redirect(url_for('wardrobe'))
```

