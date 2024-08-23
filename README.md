![Fashion Outfit Generator](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/mockup.png)


# Fashion Outfit Generator

The **Fashion Outfit Generator** is a web app that helps you create stylish outfits based on your wardrobe, occasion, and weather conditions. Add items to your virtual wardrobe, generate outfit suggestions, and get inspired for your next look!


Try it out here: [Fashion Outfit Generator](https://fashion-outfit-generator-906b3ce57bd3.herokuapp.com/outfit_suggestions)


   * [✨ Introduction](#-introduction)
      + [What It Does](#what-it-does)
      + [Why You'll Love It](#why-youll-love-it)
      + [Who It's For](#who-its-for)
   * [✨ Style](#-style)
      + [Color Scheme](#color-scheme)
      + [Styling Framework](#styling-framework)
   * [✨ Features](#-features)
      + [1. Home Page](#1-home-page)
      + [2. User Registration & Authentication](#2-user-registration-authentication)
      + [3. Personalized Wardrobe Management](#3-personalized-wardrobe-management)
      + [4. Outfit Generation Based on Weather and Occasion](#4-outfit-generation-based-on-weather-and-occasion)
      + [5. Contact Us and About Page](#5-contact-us-and-about-page)
      + [6. Responsive Design and User-Friendly Interface](#6-responsive-design-and-user-friendly-interface)
      + [7. Security Features](#7-security-features)
   * [✨ Manual Testing](#-manual-testing)
      + [1. User Registration and Login](#1-user-registration-and-login)
      + [2. Adding Items to Wardrobe](#2-adding-items-to-wardrobe)
      + [3. Editing Wardrobe Items](#3-editing-wardrobe-items)
      + [4. Outfit Generation](#4-outfit-generation)
      + [5. Search Functionality](#5-search-functionality)
      + [6. Responsive Design](#6-responsive-design)
      + [7. Accessibility Testing](#7-accessibility-testing)
      + [8. Code Validation](#8-code-validation)
      + [9. Performance Testing](#9-performance-testing)
   * [✨ Deployment](#-deployment)
   * [✨ Credits](#-credits)



## ✨ Introduction
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

## ✨ Style
### Color Scheme
The color scheme for the Fashion Outfit Generator app is designed to be both modern and visually appealing. Here are the primary colors used in the project:
![Color Palette](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/color-palette.png)
 - Primary Color: #007bff (Bootstrap Blue)
 - Secondary Color: #6c757d (Bootstrap Gray)
 - Success Color: #28a745 (Bootstrap Green)
 - Danger Color: #dc3545 (Bootstrap Red)
 - Warning Color: #ffc107 (Bootstrap Yellow)

### Styling Framework
The project utilizes Bootstrap 4.5.2 for its styling framework. Bootstrap provides a wide range of pre-designed components and utilities, allowing for responsive and attractive design without extensive custom CSS.

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

  **Example Code: User Registration and Account Creation**
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

  **Example Code: Handling User Authentication and Login**
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

  **Example Code: Setting a Default Image URL if None Provided**
```bash
if not image_url:
    image_url = url_for('static', filename='images/no-image.png')
```

- **Search Functionality**: Users can search their wardrobe by type, such as "dress" or "shoes." If the search field is empty, all wardrobe items are displayed.
![Search](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/search.png)

  **Example Code: Implementing Search Functionality in the Wardrobe**
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
![Suggestions](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/suggestions.png)

The Outfit Generation feature intelligently suggests outfits tailored to the current weather and the occasion you select. 

#### Explanation:

- **User Input**: The user selects the current weather (e.g., Spring, Summer, Autumn, Winter) and the type of occasion (e.g., Casual, Formal, Sporty).

  ![Generation](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/generation.png)

- **Smart Matching**: The app cross-references the user’s wardrobe with the selected weather and occasion. It identifies items that are suitable for the given season and matches them with the occasion type.
- **Outfit Composition**: The app randomly combines wardrobe items such as tops, bottoms, dresses, outerwear, shoes, and accessories to create complete outfits. It ensures that each suggested outfit is cohesive and appropriate for the context.
- **Three Suggestions**: Users are presented with three distinct outfit options, providing a variety of choices to suit their style and preferences.

  **Example Code: Generating Random Outfit Suggestions**
```bash
        outfit_suggestions = []
        for _ in range(3):
            outfit = {}

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
  
  **Example Code: Password Hashing with generate_password_hash**
  ```bash
      "password": generate_password_hash(request.form.get("password"))
  ```

**Strong Password Requirements**
To ensure account security, our app enforces strong password rules:
- **Minimum Length**: Passwords must be at least 8 characters.
- **Complexity**: Must include at least one uppercase letter, one lowercase letter, and one number.

**Example Code for Enforcing Strong Password Requirements in HTML Form**
  ```bash
      <div class="form-group">
          <label for="password">Password</label>
          <input type="password" class="form-control" id="password" name="password" required minlength="8" pattern="(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}">
          <small class="form-text text-muted">Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, and one number.</small>
      </div>
  ```

**Authorization Checks for Sensitive Operations**:
Certain actions, such as editing wardrobe items, require authorization to ensure that only the owner of the items or an authorized user can perform these operations. Each time an item is modified, the app verifies that the requesting user has the right permissions to carry out the action.

  **Example Code: Authorization Check Before Editing an Item**
```bash
    user_id = mongo.db.users.find_one({'username': session.get('user')})['_id']
    if item['user_id'] != user_id:
        flash('You are not authorized to edit this item.', 'danger')
        return redirect(url_for('wardrobe'))
```

## ✨ Manual Testing
This section outlines the manual testing process carried out to ensure the Fashion Outfit Generator app functions correctly. The testing was performed across multiple browsers and devices to cover a wide range of user scenarios.
### 1. User Registration and Login
**Test Scenarios:**
- **Valid Registration**: Create a new user with a unique username, valid email, and strong password. Ensure the user is redirected to their wardrobe page upon successful registration.
- **Duplicate Username**: Attempt to register with a username that already exists. Ensure that the app displays an appropriate error message and prevents registration.
- **Password Requirements**: Test the password input field by entering various combinations of characters that do not meet the required pattern (e.g., too short, missing uppercase letter). Ensure the form does not submit and displays an appropriate error message.
- **Valid Login**: Log in with a valid username and password. Ensure the user is redirected to their wardrobe page.
- **Invalid Login**: Attempt to log in with an incorrect password or non-existent username. Ensure the app displays an error message and does not log the user in.

  **Results:**

  ✅ Valid Registration: Passed

  ✅ Duplicate Username: Passed

  ✅ Password Requirements: Passed

  ✅ Valid Login: Passed

  ✅ Invalid Login: Passed


### 2. Adding Items to Wardrobe
**Test Scenarios:**
- **Valid Item Addition**: Add a new wardrobe item with all required fields filled, including an image URL. Ensure the item is saved and displayed in the user's wardrobe.

- **Empty Image URL**: Add a wardrobe item without an image URL. Ensure the item is saved with the default "no-image.png."

- **Form Validation**: Attempt to submit the form with missing fields (e.g., without selecting seasons or a color). Ensure the app displays validation errors and does not submit the form.

  **Results:**

  ✅ Valid Item Addition: Passed

  ✅ Empty Image URL: Passed

  ✅ Form Validation: Passed


### 3. Editing Wardrobe Items
**Test Scenarios:**
- **Valid Edit**: Edit an existing wardrobe item and update all fields. Ensure the item is updated correctly in the database and the changes are reflected in the wardrobe.
- **Unauthorized Edit**: Attempt to edit a wardrobe item belonging to another user by manually changing the item ID in the URL. Ensure the app prevents the edit and displays an appropriate error message.
- **Empty Image URL Handling**: Edit an item and clear the image URL field. Ensure the app does not revert to the default image unless the field is intentionally left blank.

  **Results:**

  ✅ Valid Edit: Passed

  ✅ Unauthorized Edit: Passed

  ✅ Empty Image URL Handling: Passed


### 4. Outfit Generation
**Test Scenarios:**
- **Valid Outfit Generation**: Select a season and occasion, then generate outfit suggestions. Ensure the app provides three unique outfit combinations based on the user's wardrobe.

- **Empty Wardrobe**: Attempt to generate outfits with an empty wardrobe. Ensure the app gracefully handles the situation.

- **Item Category Testing**: Test the outfit generator with wardrobes that include only certain types of items (e.g., only tops, no bottoms) to ensure the app handles missing categories appropriately.

  **Results:**

  ✅ Valid Outfit Generation: Passed

  ✅ Empty Wardrobe: Passed

  ✅ Item Category Testing: Passed


### 5. Search Functionality
**Test Scenarios:**
- **Valid Search**: Search for an item type (e.g., "dress") that exists in the wardrobe. Ensure the app returns the correct results.
- **Case Insensitivity**: Perform a search using different case variations (e.g., "Dress", "dress", "DRESS") to ensure the search function is case-insensitive.
- **Empty Search**: Submit an empty search form. Ensure the app displays all wardrobe items.

  **Results:**

  ✅ Valid Search: Passed

  ✅ Case Insensitivity: Passed

  ✅ Empty Search: Passed



### 6. Responsive Design
**Test Scenarios:**
- **Mobile Responsiveness**: Test the app on various screen sizes to ensure the layout adjusts correctly and remains usable on mobile devices.
- **Desktop Responsiveness**: Resize the browser window on a desktop to test how the layout adjusts. Ensure the content remains accessible and visually appealing.

  **Results:**

  ✅ Mobile Responsiveness: Passed

  ✅ Desktop Responsiveness: Passed

### 7. Accessibility Testing
**Test Scenarios:**
- **Keyboard Navigation:** Verify that all interactive elements (e.g., buttons, links, forms) are accessible via keyboard-only navigation.
- **Color Contrast:** Check the color contrast ratio for text and background elements to ensure readability for users with visual impairments.

  **Results:**

  ✅ Keyboard Navigation: Passed

  ✅ Color Contrast: Passed


### 8. Code Validation
**Test Scenario:**

**Python Code Validation**
- **Tool Used**: https://pep8ci.herokuapp.com/#.
- **Results**: The Python code was successfully validated, with no critical issues reported. Any warnings or suggestions for improvements were addressed.
![Python Code Validation](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/python.png)


**HTML Validation**
- **Tool Used**: [W3C Markup Validation Service](https://validator.w3.org/)
- **Results**: The HTML code was validated, and any errors identified were corrected to ensure compliance with HTML5 standards.
![HTML Code Validation](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/html.png)


**CSS Validation**
- **Tool Used**: [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)
- **Results**: The CSS code was successfully validated with no major issues.
![CSS Code Validation](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/css.png)



### 9. Performance Testing
**Test Scenario:**
Measured the time it takes for key pages (e.g., login, wardrobe, outfit generator) to load on various devices and browsers. Used Lighthouse to analyze page performance and user experience.

 - Home page:
    ![Home page Performance](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/page_home.png)

 - Login page:
  ![Login page Performance](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/page_login.png)

 - Wardrobe page:
  ![Wardrobe page Performance](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/page_wardrobe.png)

 - Outfit Generator page:
  ![Outfit Generator page Performance](https://fashion-outfit-generator.s3.eu-north-1.amazonaws.com/page_outfit_suggestions.png)

**Findings:**

 - The app performs well across tested devices and browsers, with acceptable load times for key pages. However, Lighthouse reported the presence of **third-party cookies**, which are connected to images used for wardrobe items.

    - **Details:** Lighthouse detected 17 third-party cookies, most of which are associated with images for wardrobe items. These cookies are generated by third-party image hosts that serve these images. While they currently do not significantly impact performance, Chrome and other browsers are planning to phase out support for third-party cookies as part of ongoing privacy improvements.

    - **Future Impact:** As browsers deprecate support for third-party cookies, this may affect how some images are served or loaded in the app. I will continue to monitor browser updates to ensure that all images for wardrobe items remain accessible and performant, even after third-party cookies are no longer supported.

## ✨ Deployment
To run the Fashion Outfit Generator app on your local machine, follow these instructions:

**Pre-requisites:**
- Python 3 installed on your machine.
- Git for cloning the repository.
- MongoDB installed locally or a MongoDB Atlas account for a cloud-hosted database.

**Setup Instructions:**
1. Clone the Repository:

  - Open your terminal or command prompt.

  - Clone the repository using the following command:
  ```bash
      git clone https://github.com/SShasholko/fashion-outfit-generator-in-Flask.git
  ```

  - Navigate into the project directory:
  ```bash
      cd fashion-outfit-generator-in-Flask
  ```

2. Set Up a Virtual Environment (Recommended):

  - Create a virtual environment to manage dependencies:
  ```bash
      python3 -m venv venv
  ```

  - Activate the virtual environment:
    - On Windows:
    ```bash
        venv\Scripts\activate
    ```
    - On macOS/Linux:
    ```bash
        source venv/bin/activate
    ```

3. Install Dependencies:

  - Install the required Python packages using pip:
  ```bash
    pip install -r requirements.txt
  ```

4. Configure Environment Variables:

  - Create a `.env` file in the root directory of the project 

  - Add the following environment variables to your `.env` file:
  ```bash
    IP="127.0.0.1"
    PORT="5500"
    SECRET_KEY="your-secret-key-here"
    MONGO_URI="your-mongodb-uri-here"
    MONGO_DBNAME="your-database-name-here"
  ```

5. Run the Application:
  - Start the Flask development server using the following command:
  ```bash
    python app.py
  ```

  - The app will be accessible at http://127.0.0.1:5500/.

6. Access the App:
  - Open your web browser and navigate to http://127.0.0.1:5500/ to start using the Fashion Outfit Generator on your local machine.

## ✨ Credits
This project is the result of hard work and support from some amazing individuals. I’d like to extend my heartfelt gratitude to the following people:

**Special Thanks**

  - **My Lovely Son:** Your enthusiasm, encouragement, and support have been invaluable throughout this project. Thank you for your constant inspiration and motivation.

  - **My Mentor:** Your guidance, advice, and assistance have been instrumental in the success of this project. Thank you for your invaluable input and support.

**Open Source Contributions**

This project also leverages several open-source libraries and tools, including:
   - **Flask:** A lightweight WSGI web application framework in Python, which forms the backbone of this project.
   - **Bootstrap:** For styling and responsive design, ensuring that the app looks great on all devices.
  - **MongoDB:** A NoSQL database used for storing users data and wardrobe items efficiently.