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
        flash('You must be logged in to view this page!', 'danger')
        return redirect('/')
    return dec

def no_login_required(f):
    '''Decorator for making sure user is not logged in'''
    @wraps(f)
    def dec(*args, **kwargs):
        '''dec(*args, **kwargs): Decorator for checking no login'''
        if 'osis' not in session:
            return f(*args, **kwargs)
        flash('You cannot view this page while logged in!', 'danger')
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
    print(osis)
    print(password)
    if(db_manager.userValid(osis,password)):
        session["osis"]=osis
        flash("You have successfully logged in!", "success")
        return redirect('/home')
    else:
        # flash("Wrong", 'danger')
        return redirect('/')

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash('You have logged out!', 'success')
    return redirect('/')

@app.route("/signup")
@no_login_required
def signup():
    return render_template("signup.html")

@app.route("/auth", methods=['POST'])
@no_login_required
def newUser():
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
    linfo = [combo, floor, level, type, "OWNED"]
    if(db_manager.addUser(osis, password, grade, buddy, linfo, locker, gender)=="done"):
        flash("You've successfully made an account!", 'success')
        return redirect('/')
    elif(db_manager.addUser(osis, password, grade, buddy, linfo, locker, gender)=="locker"):
        flash("Locker has already been registered.", 'danger')
        return redirect('/signup')
    else:
        flash("OSIS has already been registered.", 'danger')
        return redirect('/signup')

@app.route("/home")
@login_required
def profile():
    user = db_manager.getUserInfo(session['osis'])
    buddy = ["N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
    if len(user[4]) != 0:
        buddy = db_manager.getUserInfo(user[4])
    locker = db_manager.getLockerInfo(user[2])
    transactions = []
    if user[6] != '':
        transactions = user[6].split(",")
        for id in transactions:
            request=db_manager.getTransactionInfo(id)
            if len(request)>0:
                transactions.append(request)
    # print(transactions)
    return render_template("home.html", heading="Home", user=user, buddy=buddy, locker=locker, transactions=transactions)

@app.route("/editprof")
@login_required
def editprof():
    user = db_manager.getUserInfo(session['osis'])
    return render_template("editprof.html", user=user, heading="Edit Profile")

@app.route("/updateprof", methods=['POST'])
def updateprof():
    oldosis = session['osis']
    osis = request.form.get("osis")
    oldpassword = request.form.get("oldpassword")
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    grade = request.form.get("grade")
    locker = request.form.get("locker")
    combo = request.form.get("combo")
    type = request.form.get("location")
    level = request.form.get("level")
    floor = request.form.get("floor")
    gender = request.form.get("gender")
    if(db_manager.editUser(oldosis, osis, oldpassword, password, grade, locker, gender, combo, floor, level, type)):
        logout()
        return render_template("login.html")
    else:
        #error somewhere in the form, make more specific later
        print("error")
        return render_template("editprof.html",user=oldosis)

@app.route("/locker")
def locker():
    user = db_manager.getUserInfo(session['osis'])
    all = db_manager.tradeableLockers()
    return render_template("locker.html",user=user,all=all,results=[],heading="Locker Search")

@app.route("/lSearch", methods=['POST'])
def lSearch():
    user = db_manager.getUserInfo(session['osis'])
    searchBy = request.form.get("searchBy")
    query = request.form.get("query")
    results = db_manager.searchLocker(searchBy, query)
    #print(results)
    return render_template("locker.html", user=user,results=results)

@app.route("/lFilter", methods=['POST'])
def lFilter():
    user = db_manager.getUserInfo(session['osis'])
    floor = request.form.get("floorSearch")
    level = request.form.get("levelSearch")
    type = request.form.get("typeSearch")
    results = db_manager.filterLocker(floor,level,type)
    print(results)
    return render_template("locker.html", user=user,results=results)

if __name__ == "__main__":
    db_builder.build_db()
    app.debug = True
    app.run()
