import sqlite3
from db_builder import exec, execmany
import sys
import random
from datetime import datetime
from datetime import timedelta
from flask import flash

def userValid(osis,password):
    q = "SELECT password from user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    if (data is not None):
        if (data[0] == password):
            return True
        else:
            flash("Incorrect OSIS and password combination.", 'danger')
            return False
    flash("OSIS does not exist. Please sign up for an account.", 'danger')
    return False

def addUser(osis, password, grade, buddy, linfo, locker, gender):
    q = "SELECT * FROM user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    if (data is None):
        q = "SELECT * FROM locker_tbl WHERE locker=?"
        inputs = (locker,)
        data = execmany(q, inputs).fetchone()
        if(data is None):
            q = "INSERT INTO user_tbl VALUES(?, ?, ?, ?, ?, ?, ?)"
            inputs = (osis, password, locker, grade, buddy, "", gender)
            execmany(q, inputs)
            q = "INSERT INTO locker_tbl VALUES(?, ?, ?, ?, ?, ?, ?)"
            inputs = (locker, osis, linfo[0], linfo[1], linfo[2], linfo[3], linfo[4])
            execmany(q, inputs)
            return "done"
        else:
            return "locker"
    return "user"

def getUserInfo(osis):
    q = "SELECT * from user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    info = [data[0],data[1],data[2],data[3],data[4],data[5],data[6]]
    return info

def getLockerInfo(locker):
    q = "SELECT * from locker_tbl WHERE locker=?"
    inputs = (locker,)
    data = execmany(q, inputs).fetchone()
    info = [data[0],data[1],data[2],data[3],data[4],data[5],data[6]]
    return info

def editUserTbl(osis,fxn,new):
    new = "\"" + new + "\""
    q = "UPDATE user_tbl SET " + fxn + "=" + new + " WHERE osis=?"
    inputs = (osis,)
    data = execmany(q,inputs)
    return True

def editLockerTbl(locker,fxn,new):
    new = "\"" + new + "\""
    q = "UPDATE locker_tbl SET " + fxn + "=" + new + " WHERE locker=?"
    inputs = (locker,)
    data = execmany(q,inputs)
    return True

def editUser(oldosis, osis, oldpassword, password, grade, locker, gender, combo, floor, level, type):
    if(userValid(oldosis,oldpassword)):
        if (password != ""): editUserTbl(oldosis,"password",password)
        if (grade != ""): editUserTbl(oldosis,"grade", grade)
        if (gender != ""): editUserTbl(oldosis,"gender", gender)
        q = "SELECT locker FROM user_tbl WHERE osis=?"
        inputs = (oldosis,)
        oldlocker = execmany(q,inputs).fetchone()[0]
        if (combo != ""): editLockerTbl(oldlocker,"combo", combo)
        if (floor != ""): editLockerTbl(oldlocker,"floor", floor)
        if (level != ""): editLockerTbl(oldlocker,"level", level)
        if (type != ""): editLockerTbl(oldlocker,"location", type)
        if (locker != ""):
            editLockerTbl(oldlocker, "locker", locker)
            editUserTbl(oldosis, "locker", locker)
        if (osis != ""):
            q = "UPDATE locker_tbl SET owner=? WHERE owner=?"
            inputs = (osis,oldosis)
            data = execmany(q, inputs)
            editUserTbl(oldosis,"osis",osis)
        return True
    return False

#creates dict of transaction/locker data given list of tuples
def getTransLock(data):
    dataDict = {}
    for i in data:
        lock = getLockerInfo(i[0])
        dataDict[i] = lock
    return dataDict

#returns a dict of transaction_tbl tuples and locker_tbl lists of all available lockers
def tradeableLockers():
    q = "SELECT * FROM transaction_tbl WHERE status=1 AND request='L'"
    data = exec(q).fetchall() #-> [(tuple,1,2,3),(tuple,1,2,3)]
    return getTransLock(data)

#returns a dict of transaction_tbl tuple and locker_tbl list of searched locker
def searchLocker(searchBy, query):
    if (searchBy == "Locker Number"):
        if (len(query) != 5):
            return False
        head,space,tail = query.partition(" ")
        q = "SELECT * FROM transaction_tbl WHERE locker=" + tail + " AND floor=" + head
    else:
        if (len(query) != 9):
            return False
        q = "SELECT * FROM transaction_tbl WHERE sender=" + query
    data = exec(q).fetchall()
    return getTransLock(data)

#  transaction_tbl (locker INT, recipient INT, sender INT, status '1=OPEN,0=CLOSED ', request 'L or B', floor INT)
#  locker_tbl (locker INT, owner TEXT, combo TEXT, floor INT, level INT, location TEXT, status 'OWNED,TRADING,BUDDY')


def filterLocker(floor,level,location):
    q = "SELECT owner FROM locker_tbl WHERE status='TRADING'"
    if (floor != ""):
        q += " AND floor=" + floor
    if (level != ""):
        q += " AND level='" + level + "'"
    if (location != ""):
        q += " AND location='" + location + "'"
    data = exec(q).fetchall()
    dictRes = {}
    for i in data:
        dictRes.update(searchLocker("Owner", i[0]))
    return dictRes
