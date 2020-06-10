import sqlite3
from db_builder import exec, execmany
import sys
import random
from datetime import datetime
from datetime import timedelta

def userValid(osis,password):
    q = "SELECT password from user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    if (data is not None):
        if (data[0] == password):
            return True
        else:
            return False
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
            q = "INSERT INTO user_tbl VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
            inputs = (osis, password, locker, grade, buddy, "", "", gender)
            execmany(q, inputs)
            q = "INSERT INTO locker_tbl VALUES(?, ?, ?, ?, ?, ?, ?)"
            inputs = (locker, osis, linfo[0], linfo[1], linfo[2], linfo[3], linfo[4])
            execmany(q, inputs)
            return "done"
        else:
            "locker"
    return "user"

def getUserInfo(osis):
    q = "SELECT * from user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    info = [data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]]
    return info

def getLockerInfo(locker):
    q = "SELECT * from locker_tbl WHERE locker=?"
    inputs = (locker,)
    data = execmany(q, inputs).fetchone()
    info = [data[0],data[1],data[2],data[3],data[4],data[5],data[6]]
    return info

def getTransactionInfo(id):
    q = "SELECT * from transaction_tbl WHERE id=?"
    inputs = (id,)
    data = execmany(q, inputs).fetchone()
    info = []
    if(data is None):
        return info
    if data[4] == "open":
        info = [data[0],data[1],data[2],data[3],data[4],data[5]]
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
        if (grade != "No Change"): editUserTbl(oldosis,"grade", grade)
        if (gender != "No Change"): editUserTbl(oldosis,"gender", gender)
        q = "SELECT locker FROM user_tbl WHERE osis=?"
        inputs = (oldosis,)
        oldlocker = execmany(q,inputs).fetchone()[0]
        if (combo != ""): editLockerTbl(oldlocker,"combo", combo)
        if (floor != "No Change"): editLockerTbl(oldlocker,"floor", floor)
        if (level != "No Change"): editLockerTbl(oldlocker,"level", level)
        if (type != "No Change"): editLockerTbl(oldlocker,"location", type)
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

#creates dict of transaction/locker data
def getTransLock(data):
    dataDict = {}
    for i in data:
        lock = getLockerInfo(i[1])
        dataDict[i] = lock
    return dataDict

#returns a dict of transaction_tbl tuples and locker_tbl lists of all available lockers
def tradeableLockers():
    q = "SELECT * FROM transaction_tbl WHERE status='OPEN' AND request='trade'"
    data = exec(q).fetchall() #-> [(tuple,1,2,3),(tuple,1,2,3)]
    return getTransLock(data)

#returns a dict of transaction_tbl tuple and locker_tbl list of searched locker
def searchLocker(searchBy, query):
    if (searchBy == "Locker Number"):
        head,space,tail = query.partition(" ")
        q = "SELECT * FROM transaction_tbl WHERE locker=" + tail + " AND floor=" + head
    else:
        q = "SELECT * FROM transaction_tbl WHERE sender=" + query
    data = exec(q).fetchall()
    return getTransLock(data)

#  transaction_tbl (id INT, locker INT, recipient INT, sender INT, status TEXT, request TEXT)
#  locker_tbl (locker INT, owner TEXT, combo TEXT, floor INT, level INT, location TEXT, status TEXT)


def filterLocker(floor,level,location):
    q = "SELECT owner FROM locker_tbl WHERE status='OPEN'"
    if (floor != ""):
        q += " AND floor=" + floor
    if (level != ""):
        q += " AND level='" + level + "'"
    if (type != ""):
        q += " AND location='" + location + "'"
    print(q)
    data = exec(q).fetchall()
    dictRes = {}
    for i in data:
        dictRes.update(searchLocker("Owner", i[0]))
    return dictRes
