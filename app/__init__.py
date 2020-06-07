# Team Deluxe-Tardigrades :: Yifan Wang, Amber Chen, Elizabeth Doss, Mandy Zheng
# SoftDev pd1
# P05 :: Fin
# 2020-06-11

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import date, timedelta
import db_builder, db_manager
import os, random, sqlite3
import urllib3, json, urllib

app = Flask(__name__)
app.secret_key = os.urandom(32)

def login_required(f):
    @wraps(f)
    def dec(*args, **kwargs):
        '''dec (*args, **kwargs): Decorator for checking login and if user in session'''
        if 'osis' in session:
            return f(*args, **kwargs)
        flash('You must be logged in to view this page!', 'alert-danger')
        return redirect('/')
    return dec

def no_login_required(f):
    '''Decorator for making sure user is not logged in'''
    @wraps(f)
    def dec(*args, **kwargs):
        '''dec(*args, **kwargs): Decorator for checking no login'''
        if 'osis' not in session:
            return f(*args, **kwargs)
        flash('You cannot view this page while logged in!', 'alert-danger')
        return redirect('/home')
    return dec

@app.route("/")
@no_login_required
def login():
    return render_template("login.html")

@app.route("/check", methods=['POST'])
@no_login_required
def authentication():
    osis = request.form.get("osis")
    password = request.form.get("password")
    if(userValid(osis,password)):
        session["osis"]=osis
        return render_template("home.html")
    else:
        #wrong credentials flash message
        return render_template("login.html")

@app.route("/signup")
@no_login_required
def signup():
    return render_template("signup.html")

@app.route("/auth", methods=['POST'])
@no_login_required
def newUser():
    #add error handling (like password mismatch and invalud stuff), blank fields, and flash
    osis = request.form.get("osis")
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    grade = request.form.get("grade")
    locker = request.form.get("locker")
    combo = request.form.get("combo")
    type = request.form.get("location")
    level = request.form.get("level")
    floor = request.form.get("floor")
    gender = request.form.get("gender")
    buddy = ""
    survey = combo+","+floor+","+level+","+type+",OWNED"
    if(db_manager.addUser(osis, password, grade, buddy, survey, locker, gender)=="done"):
        return render_template("login.html")
    elif(db_manager.addUser(osis, password, grade, buddy, survey, locker, gender)=="locker"):
        #someone already registered locker add flash
        return render_template("signup.html")
    else:
        #someone already registered with that osis add flash
        return render_template("signup.html")

if __name__ == "__main__":
    db_builder.build_db()
    app.debug = True
    app.run()
