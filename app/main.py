from flask import Flask, render_template, make_response
from flask import request, redirect
import pandas as pd


app = Flask(__name__)


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
