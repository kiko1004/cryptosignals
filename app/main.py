from flask import Flask, render_template, make_response
from flask import request, redirect
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy_utils.functions import database_exists
from dotenv import load_dotenv
try:
    load_dotenv()
except:
    pass



SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)

class freemember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    country = db.Column(db.String(120))
    company = db.Column(db.String(120))
    experience = db.Column(db.String(120))
    referalcode = db.Column(db.String(120))
    targetmoney = db.Column(db.String(120))
    signals = db.Column(db.Integer)

class premiummember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    country = db.Column(db.String(120))
    company = db.Column(db.String(120))
    experience = db.Column(db.String(120))
    referalcode = db.Column(db.String(120))
    targetmoney = db.Column(db.String(120))


db.create_all()



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/login")
def signals():
    return render_template('login.html')

@app.route("/premiumrequest/<data>")
def route_two(data):
  return render_template("premium.html", type=data)


@app.route("/signupfree", methods=["GET", "POST"])
def signupfree():
    if request.method == "POST":
        req = request.form
        username = req.get("username")
        password = req.get("password")
        first_name = req.get("first_name")
        last_name = req.get("last_name")
        email = req.get("email")
        country = req.get("country")
        phone_number = req.get("phone_number")
        prevex = req.get("meal_preference")
        reff = req.get("reff")
        company = req.get("company")
        money=req.get("money")
        newmember = freemember(name=first_name, username=username, password=password, surname=last_name,
                               email=email, phone=phone_number, country=country, company=company, experience=prevex,
                               referalcode=reff, targetmoney=money, signals=5)
        db.session.add(newmember)
        try:
            db.session.commit()
        except:
            db.session.rollback()






    return render_template('signup.html')