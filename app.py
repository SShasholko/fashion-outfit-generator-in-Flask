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


if __name__ == '__main__':
    app.run(
        host = os.environ.get('IP', IP),
        port = int(os.environ.get('PORT', PORT)),
        debug=True)