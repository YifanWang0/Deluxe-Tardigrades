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
    if(db_manager.userValid(osis,password)):
        session["osis"]=osis
        return redirect('/home')
    else:
        flash("Wrong")
        return redirect('/')

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash('You have logged out!')
    return redirect('/')

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
    linfo = [combo, floor, level, type, "OWNED"]
    if(db_manager.addUser(osis, password, grade, buddy, linfo, locker, gender)=="done"):
        flash("You've successfully made an account!")
        return redirect('/')
    elif(db_manager.addUser(osis, password, grade, buddy, linfo, locker, gender)=="locker"):
        #someone already registered locker add flash
        return redirect('/signup')
    else:
        #someone already registered with that osis add flash
        return redirect('/signup')

@app.route("/home")
@login_required
def profile():
    user = db_manager.getUserInfo(session['osis'])
    buddy = ["N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
    if len(user[4]) != 0:
        buddy = db_manager.getUserInfo(user[4])
    locker = db_manager.getLockerInfo(user[2])
    transactions=db_manager.getTransactionInfo(session['osis'])
    return render_template("home.html", heading="Profile", user=user, buddy=buddy, locker=locker, transactions=transactions)

@app.route("/updated", methods=['POST'])
@login_required
def updateBuddy():
     osis=request.form.get("request")
     db_manager.buddyRequest(osis,session['osis'])
     return redirect("/home")

@app.route("/editprof", methods=['POST'])
def editprof():
    return render_template("editprof.html")

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
        return render_template("login.html")
    else:
        #error somewhere in the form, make more specific later
        print("error")
        return render_template("editprof.html")

@app.route("/survey")
@login_required
def survey():
    sports = ""
    books = ""
    misc = ""
    list = db_manager.getSurveyInfo(session["osis"])
    if (len(list)>0):
        sports = list[0]
        books = list[1]
        misc = list[2]
    return render_template("survey.html", sports = sports, books = books, misc = misc)

@app.route("/buddy", methods=['POST'])
@login_required
def buddy():
    sports = request.form.get("sports")
    books = request.form.get("textbook")
    misc = request.form.get("misc")
    info = sports+","+books+","+misc
    db_manager.updateSurvey(session['osis'],info)
    return render_template("buddy.html", query=["","","","","","","","",""])

@app.route("/bsearch", methods=['POST'])
@login_required
def bsearch():
    query=["","","","","","","","",""]
    if request.form.get("searchtype") == "osis":
        query[0] = request.form.get("input")
    else:
        query[1] = request.form.get("input")
    query[2] = request.form.get("sports")
    query[3] = request.form.get("textbook")
    query[4] = request.form.get("grade")
    query[5] = request.form.get("gender")
    query[6] = request.form.get("floor")
    query[7] = request.form.get("location")
    query[8] = request.form.get("level")
    results = db_manager.filter(query,session["osis"])
    buddy=[]
    locker=[]
    loop=[]
    survey =[]
    count = 0
    for value in range(len(results)):
        info = db_manager.getUserInfo(results[value])
        buddy.append(info)
        temp=db_manager.getLockerInfo(info[2])
        locker.append(temp)
        loop.append(count)
        temp=["", ""]
        if info[5] != "":
            temp = info[5].split(",")
        survey.append(temp)
        count+=1
    to = db_manager.getTransactionTo(session["osis"])
    sender = db_manager.getTransactionFrom(session["osis"])
    return render_template("buddy.html" , query=query,buddy=buddy,locker=locker, to = to, sender = sender, loop=loop, survey=survey)
if __name__ == "__main__":
    db_builder.build_db()
    app.debug = True
    app.run()
