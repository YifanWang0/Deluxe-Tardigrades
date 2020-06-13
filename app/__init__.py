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
    if(db_manager.userValid(osis,password)):
        session["osis"]=osis
        flash("You have successfully logged in!", "success")
        return redirect('/home')
    else:
        # flash("Wrong Login Information!", 'danger')
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
    if (locker == ""):
        linfo[4] = ""
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
    userInfo = db_manager.getUserInfo(session['osis'])
    buddy = ["N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
    if userInfo[4] != "":
        buddy = db_manager.getUserInfo(userInfo[4])
    locker = db_manager.getLockerInfo(userInfo[2], session['osis'])
    transactions=db_manager.getTransactionInfo(session['osis'])
    changed=db_manager.ifDissolve(session["osis"])
    return render_template("home.html", heading="Profile", userInfo=userInfo, buddy=buddy, locker=locker, transactions=transactions , user=session['osis'], changed=changed)

@app.route("/updated", methods=['POST'])
@login_required
def updateBuddy():
     osis=request.form.get("request")
     db_manager.buddyRequest(osis,session['osis'])
     return redirect("/home")

@app.route("/giveup", methods=['POST'])
@login_required
def giveUp():
    osis1 = session["osis"]
    osis2 = request.form.get("person")
    type = request.form.get("type")
    if(request.form.get("return")=="home"):
        db_manager.deleteTrans(osis1,osis2,type)
    else:
        db_manager.deleteTrans(osis2,osis1,type)
        db_manager.deleteTrans(osis1,osis2,type)
    return redirect("/"+request.form.get("return"))

@app.route("/confirm", methods=['POST'])
@login_required
def confirm():
     osis1 = request.form.get("person")
     print(osis1)
     osis2 = session["osis"]
     type = request.form.get("type")
     if (type == "B"):
         db_manager.confirmB(osis1,osis2)
     if (type == "L"):
         db_manager.acceptLocker(osis2,osis1)
     if (type == "D"):
         db_manager.dissolveBuddy(osis2, osis1)
     return redirect("/home")

@app.route("/dissolve", methods=['POST'])
@login_required
def breakBuddy():
     osis=request.form.get("break")
     db_manager.breakB(session['osis'], osis)
     return redirect("/home")

@app.route("/editprof")
@login_required
def editprof():
    user = session['osis']
    return render_template("editprof.html", user=user, heading="Edit Profile")

@app.route("/updateprof", methods=['POST'])
@login_required
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
        flash("Error",'danger')
        return render_template("editprof.html",heading="Edit Profile",user=oldosis)

@app.route("/survey")
@login_required
def survey():
    info=db_manager.getUserInfo(session["osis"])
    if(info[4]!=""):
        flash("Sorry! You already have a Buddy!",'danger')
        return redirect("/home")
    sports = ""
    books = ""
    misc = ""
    user = session['osis']
    list = db_manager.getSurveyInfo(session["osis"])
    if (len(list)>0):
        sports = list[0]
        books = list[1]
        misc = list[2]
    return render_template("survey.html", heading = "Lockey Buddy Survey", sports = sports, books = books, misc = misc, user=user)

@app.route("/buddy", methods=['POST'])
@login_required
def buddy():
    sports = request.form.get("sports")
    books = request.form.get("textbook")
    misc = request.form.get("misc")
    info = sports+","+books+","+misc
    db_manager.updateSurvey(session['osis'],info)
    user=session['osis']
    return render_template("buddy.html", heading = "Lockey Buddy Search", query=["","","","","","","","",""], user=user)

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
    length=len(results)
    buddy=[]
    locker=[]
    loop=[]
    survey =[]
    count = 0
    for value in range(len(results)):
        info = db_manager.getUserInfo(results[value])
        buddy.append(info)
        temp=db_manager.getLockerInfo(info[2],session['osis'])
        locker.append(temp)
        loop.append(count)
        temp=["", ""]
        if info[5] != "":
            temp = info[5].split(",")
        survey.append(temp)
        count+=1
    to = db_manager.getTransactionTo(session["osis"])
    sender = db_manager.getTransactionFrom(session["osis"])
    user=session['osis']
    return render_template("buddy.html" , query=query,buddy=buddy,locker=locker, to = to, sender = sender, loop=loop, survey=survey, length=length, user=user)

@app.route("/locker")
@login_required
def locker():
    user = session['osis']
    all = db_manager.tradeableLockers()
    to = db_manager.getTransactionTo(session["osis"])
    sender = db_manager.getTransactionFrom(session["osis"])
    return render_template("locker.html",user=user,all=all,results=[],to=to,sender=sender,heading="Locker Search")

@app.route("/lSearch", methods=['POST'])
@login_required
def lSearch():
    user = session['osis']
    searchBy = request.form.get("searchBy")
    query = request.form.get("query")
    results = db_manager.searchLocker(searchBy, query)
    to = db_manager.getTransactionTo(session["osis"])
    sender = db_manager.getTransactionFrom(session["osis"])
    if (not results and results != {}):
        flash("Incorrect Query Format","danger")
        return redirect('/locker')
    return render_template("locker.html",heading="Locker Search",to=to,sender=sender,user=user,results=results)

@app.route("/lFilter", methods=['POST'])
@login_required
def lFilter():
    user = session['osis']
    floor = request.form.get("floorSearch")
    level = request.form.get("levelSearch")
    type = request.form.get("typeSearch")
    to = db_manager.getTransactionTo(session["osis"])
    sender = db_manager.getTransactionFrom(session["osis"])
    results = db_manager.filterLocker(floor,level,type)
    return render_template("locker.html",heading="Locker Search",to=to,sender=sender,user=user,results=results)

@app.route("/market", methods=['POST'])
@login_required
def market():
    user = session['osis']
    locker = db_manager.getUserInfo(user)[2]
    if (db_manager.getLockerInfo(locker,user)[6] == 'TRADING'):
        flash("Locker already on market!", 'danger')
        return redirect('/home')
    db_manager.putOnMarket(locker,user)
    return redirect("/home")

@app.route("/lRequest", methods=['POST'])
@login_required
def lRequest():
     user = session['osis']
     osis=request.form.get("lrequest")
     db_manager.lockerRequest(osis,user)
     return redirect("/home")

@app.route("/lAccept", methods=['POST'])
@login_required
def lAccept():
     me = session['osis']
     you=request.form.get("laccept")
     db_manager.acceptLocker(me,you)
     return redirect("/home")

@app.route("/notifs")
@login_required
def notifs():
    looper=[]
    buddy=[]
    locker=[]
    dissolve = []
    all = db_manager.getAllNotifs(session["osis"])
    for value in range(len(all)):
        looper.append(value)
    for value in all:
        if(value[4] == "B"):
            temp=db_manager.getUserInfo(value[2],session['osis'])
            temp[5]=temp[5].split(",")
            buddy.append(temp)
        if(value[4] == "L"):
            them = db_manager.getUserInfo(value[2])
            print(them)
            locker.append(db_manager.getLockerInfo(them[2],them[0]))
        else:
            dissolve.append(db_manager.getDissolveInfo(session['osis']))
    open = db_manager.getMess(session["osis"],1)
    close = db_manager.getMess(session["osis"],0)
    user=session['osis']
    return render_template("notifs.html", all=all, open=open, close=close, looper=looper, buddy=buddy, locker=locker, dissolve = dissolve, user=user)

if __name__ == "__main__":
    db_builder.build_db()
    app.debug = True
    app.run()
