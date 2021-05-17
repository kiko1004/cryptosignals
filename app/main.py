from flask import Flask, render_template, make_response
from flask import request, redirect
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy_utils.functions import database_exists
from dotenv import load_dotenv
from datetime import date

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
    username = db.Column(db.String(80), unique=True)
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


class requestedsignals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120))
    coin = db.Column(db.String(120))
    typeofanalysis = db.Column(db.String(120))
    date = db.Column(db.String(120))


db.create_all()


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route("/login")
def login():
    username = request.cookies.get('username')
    return render_template('login.html', username=username)


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
        money = req.get("money")
        ifuser = freemember.query.filter(freemember.username == username).first()
        newmember = freemember(name=first_name, username=username, password=password, surname=last_name,
                               email=email, phone=phone_number, country=country, company=company, experience=prevex,
                               referalcode=reff, targetmoney=money, signals=5)
        if ifuser is None:
            db.session.add(newmember)
            try:
                db.session.commit()
                resp = make_response(render_template("login.html", username=username))
                resp.set_cookie('username', username)

                return resp
            except:
                db.session.rollback()
        else:
            return "<h1>User already exists</h1>"

    return render_template('signup.html')


@app.route("/premiumrequest/signuppremium", methods=["GET", "POST"])
def signuppremium():
    if request.method == "POST":
        req = request.form
        first_name = req.get("first_name")
        last_name = req.get("last_name")
        email = req.get("email")
        country = req.get("country")
        phone_number = req.get("phone_number")
        prevex = req.get("meal_preference")
        reff = req.get("reff")
        company = req.get("company")
        money = req.get("money")
        newmember = premiummember(name=first_name, surname=last_name,
                                  email=email, phone=phone_number, country=country, company=company, experience=prevex,
                                  referalcode=reff, targetmoney=money)
        db.session.add(newmember)
        try:
            db.session.commit()

        except:
            db.session.rollback()
    return "<h1>Your requset has been sent. You will receive a call soon.</h1>"


@app.route("/loginpost", methods=["GET", "POST"])
def loginpost():
    if request.method == "POST":
        req = request.form
        username = req.get("username")
        password = req.get("password")
        logeduser = freemember.query.filter(freemember.username == username).first()
        if logeduser is not None:
            if logeduser.password == password:
                signals = logeduser.signals
                resp = make_response(
                    render_template("signals.html", username=username, isLoggedin="True", signals=signals))
                resp.set_cookie('username', username)
                resp.set_cookie('isLoggedin', "True")
                return resp
            elif logeduser is not None:
                return "<h1>Wrong Password</h1>"
        else:
            return "<h1>No such User</h1>"


@app.route("/signals")
def signals():
    username = request.cookies.get('username')
    isLoggedin = request.cookies.get('isLoggedin')
    logeduser = freemember.query.filter(freemember.username == username).first()
    try:
        signals = logeduser.signals
    except:
        signals = 0

    return render_template('signals.html', username=username, isLoggedin=isLoggedin, signals=signals)


@app.route("/requestsignal", methods=["GET", "POST"])
def signalsrequest():
    username = request.cookies.get('username')
    isLoggedin = request.cookies.get('isLoggedin')
    logeduser = freemember.query.filter(freemember.username == username).first()
    try:
        signals = logeduser.signals
    except:
        signals

    if request.method == "POST":
        req = request.form
        coin = req.get("coin")
        analysis = req.get("typeofanal")
        if signals <= 0:
            return render_template('signals.html', username=username, isLoggedin=isLoggedin, signals=signals,
                                   message="You have used all your free signals.")
        signals = signals - 1
        logeduser.signals = signals
        db.session.commit()
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")

        newrequest = requestedsignals(user=username, coin=coin, typeofanalysis=analysis, date=d1)
        db.session.add(newrequest)
        try:
            db.session.commit()
        except:
            db.session.rollback()

        return render_template('signals.html', username=username, isLoggedin=isLoggedin, signals=signals,
                               message="Signal request sent successfully!")

    return render_template('signals.html', username=username, isLoggedin=isLoggedin, signals=signals)


@app.route("/adminpanel", methods=["GET", "POST"])
def adminPanel():
    freeusers = freemember.query.all()
    premiumusers = premiummember.query.all()
    requests = requestedsignals.query.all()
    if request.method == "POST":
        req = request.form
        password = req.get("adminpass")
        resp = make_response(render_template("adminpanel.html", adminpass=password, freeusers=freeusers,
                                             premiumusers=premiumusers, requests=requests))
        resp.set_cookie('adminpass', password)
        return resp
    else:
        password = request.cookies.get('adminpass')
        return render_template("adminpanel.html", adminpass=password, freeusers=freeusers, premiumusers=premiumusers,
                               requests=requests)
