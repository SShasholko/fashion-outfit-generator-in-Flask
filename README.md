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