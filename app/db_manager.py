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
        if (locker != ""):
            q = "SELECT * FROM locker_tbl WHERE locker='" + locker + "' AND floor='" + linfo[1] + "'"
            data = exec(q).fetchone()
        if(data is None or locker==""):
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
    info=[]
    for value in data:
        info.append(value)
    return info

def getTransactionInfo(osis):
    q = "SELECT * from transaction_tbl WHERE sender=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchall()
    info = []
    # print(q)
    if(data is None):
        return info
    for value in data:
        # print(value)
        # print(len(value))
        # print(value[4])
        if len(value)>0 and value[3] == 1:
            info.append([value[0],value[1],value[2],value[3],value[4],value[5]])
    return info

def getSurveyInfo(osis):
    q = "SELECT survey from user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    info = []
    if(data[0] != ""):
        info = data[0].split(",")
    return info

def updateSurvey(osis, info):
    q = "UPDATE user_tbl SET survey=? WHERE osis=?"
    inputs = (info, osis)
    execmany(q, inputs)

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
    q = "SELECT * FROM transaction_tbl WHERE status=1 AND request='L' AND recipient=''"
    data = exec(q).fetchall() #-> [(tuple,1,2,3),(tuple,1,2,3)]
    return getTransLock(data)

#returns a dict of transaction_tbl tuple and locker_tbl list of searched locker
def searchLocker(searchBy, query):
    if (searchBy == "Locker Number"):
        if (len(query) != 5):
            return False
        head,space,tail = query.partition("-")
        q = "SELECT * FROM transaction_tbl WHERE recipient='' AND locker=" + tail + " AND floor=" + head
    else:
        if (len(query) != 9):
            return False
        q = "SELECT * FROM transaction_tbl WHERE recipient='' AND sender=" + query
    data = exec(q).fetchall()
    return getTransLock(data)

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

def filter(query,osis):
    q="SELECT osis FROM user_tbl WHERE osis != " + osis
    info=[]
    if query[0] != "":
        q+="AND osis = '" + query[0]+"'"
    if query[1] != "":
        q+="AND locker = '" + query[1]+"'"
    if query[2] != "" and  query[2] != "None":
        q+=" AND survey LIKE '%" + query[2] +"%'"
    if query[3] != "" and  query[3] != "None":
        q+=" AND survey LIKE '%" + query[3] +"%'"
    if query[4] != "" and  query[4] != "None":
        q+=" AND grade = '" + query[4]+"'"
    if query[5] != "" and  query[5] != "None":
        q+=" AND gender = '" + query[5]+"'"
    if query[6] != "" and  query[6] != "None":
        q+=" AND floor = '" + query[6]+"'"
    if query[7] != "" and  query[7] != "None":
        q+=" AND location = '" + query[7]+"'"
    if query[8] != "" and  query[8] != "None":
        q+=" AND level = '" + query[8]+"'"
    q+=";"
    data=exec(q).fetchall()
    for value in data:
        info.append(str(value[0]))
    return info

def getTransactionFrom(osis):
    q="SELECT recipient FROM transaction_tbl WHERE sender=?"
    inputs = (osis,)
    data = execmany(q,inputs).fetchall()
    info=[]
    if data is None:
        return info
    for value in data:
        info.append(value[0])
    filtered = [x for x in info if x != '']
    return filtered

def getTransactionTo(osis):
    q="SELECT sender FROM transaction_tbl WHERE recipient=?"
    inputs = (osis,)
    data = execmany(q,inputs).fetchall()
    info=[]
    # print(q)
    if data is None:
        return info
    for value in data:
        info.append(value[0])
    # print(info)
    return info

def buddyRequest(to, sender):
    locker = getUserInfo(to)
    if locker == '':
        locker = getUserInfo(sender)[2]
    q = "INSERT INTO transaction_tbl VALUES (?,?,?,?,?,?)"
    inputs=(locker[2],to, sender, 1, "B", locker[3])
    execmany(q,inputs)

def putOnMarket(locker):
    linfo = getLockerInfo(locker)
    q = "INSERT INTO transaction_tbl VALUES (?,?,?,?,?,?)"
    inputs = (locker,"",linfo[1],1,'L',linfo[3])
    execmany(q,inputs)
    q = "UPDATE locker_tbl SET status='TRADING' WHERE locker=" + str(locker)
    exec(q)

#  user_tbl (osis INT, password TEXT, locker INT, grade INT, buddy INT, survey TEXT, gender TEXT)"
#  locker_tbl (locker INT, owner TEXT, combo TEXT, floor INT, level INT, location TEXT, status 'OWNED,TRADING,BUDDY')
#  transaction_tbl (locker INT, recipient INT, sender INT, status '1=OPEN,0=CLOSED ', request 'L or B', floor INT)

def lockerRequest(to,sender):
    owner = getUserInfo(to)
    locker = getLockerInfo(owner[2])
    q = "INSERT INTO transaction_tbl VALUES (?,?,?,?,?,?)"
    inputs=(owner[2],to, sender, 1, "L", locker[3])
    execmany(q,inputs)

def giveUp(sender,recipient):
    if (recipient == ""):
        q = "UPDATE locker_tbl SET status='OWNED' WHERE owner=" + sender
        exec(q)
        q = "DELETE FROM transaction_tbl WHERE sender=" + sender + " AND recipient=''"
    else:
        q = "DELETE FROM transaction_tbl WHERE sender=" + sender + " AND recipient=" + recipient
    print(q)
    exec(q)

def acceptLocker(me,you):
    owner = getUserInfo(me)
    ownerL = getLockerInfo(owner[2])
    recipient = getUserInfo(you)
    recipientL = getLockerInfo(recipient[2])
    q = "UPDATE user_tbl SET locker=" + str(recipient[2]) + " WHERE osis=" + str(me)
    exec(q)
    q = "UPDATE user_tbl SET locker=" + str(owner[2]) + " WHERE osis=" + str(you)
    exec(q)
    q = "UPDATE locker_tbl SET status='OWNED',locker=" + str(recipientL[0]) + ",combo=" + str(recipientL[2]) + ",floor=" + str(recipientL[3]) + ",level='" + str(recipientL[4]) + "',location='" + str(recipientL[5]) + "' WHERE owner=" + str(me)
    exec(q)
    q = "UPDATE locker_tbl SET status='OWNED',locker=" + str(ownerL[0]) + ",combo=" + str(ownerL[2]) + ",floor=" + str(ownerL[3]) + ",level='" + str(ownerL[4]) + "',location='" + str(ownerL[5]) + "' WHERE owner=" + str(you)
    exec(q)
    q = "UPDATE transaction_tbl SET status=0 WHERE recipient=" + str(me) + " AND sender=" + str(you) + " AND request='L'"
    exec(q)
    giveUp(me,'')
    giveUp(you,'')
