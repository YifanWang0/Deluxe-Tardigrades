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
            q = "INSERT INTO user_tbl VALUES(?, ?, ?, ?, ?, ?, ?)"
            inputs = (osis, password, locker, grade, buddy, "", gender)
            execmany(q, inputs)
            q = "INSERT INTO locker_tbl VALUES(?, ?, ?, ?, ?, ?, ?)"
            inputs = (locker, osis, linfo[0], linfo[1], linfo[2], linfo[3], linfo[4])
            execmany(q, inputs)
            return "done"
        else:
            "locker"
    return "user"

def getUserInfo(osis):
    q = "SELECT * from user_tbl WHERE osis = " + osis + ";"
    data = exec(q).fetchone()
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
    print(q)
    if(data is None):
        return info
    for value in data:
        print(value)
        print(len(value))
        print(value[4])
        if len(value)>0 and value[3] == 1:
            info.append([value[0],value[1],value[2],value[3],value[4]])
    print(info)
    return info


def getSurveyInfo(osis):
    q = "SELECT survey from user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    info = []
    if(data[0] != ""):
        info = data[0].split(",")
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

def updateSurvey(osis, info):
    q = "UPDATE user_tbl SET survey=? WHERE osis=?"
    inputs = (info, osis)
    execmany(q, inputs)


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
    return info

def getTransactionTo(osis):
    q="SELECT sender FROM transaction_tbl WHERE recipient=?"
    inputs = (osis,)
    data = execmany(q,inputs).fetchall()
    info=[]
    if data is None:
        return info
    for value in data:
        info.append(value[0])
    return info

def buddyRequest(to, sender):
    locker = getUserInfo(to)[2]
    if locker == '':
        locker = getUserInfo(sender)[2]
    q = "INSERT INTO transaction_tbl VALUES (?,?,?,?,?)"
    inputs=(locker,to, sender, 1, "B")
    execmany(q,inputs)

def getMess(osis,num):
    q="SELECT * FROM transaction_tbl WHERE recipient=? AND status = ?"
    inputs = (osis,num)
    data = execmany(q,inputs).fetchall()
    info=[]
    temp=[]
    if data is None:
        return info
    for value in data:
        for cell in value:
            temp.append(cell)
        info.append(temp)
    return info

def getAllNotifs(osis):
    q="SELECT * FROM transaction_tbl WHERE recipient=?"
    inputs = (osis,)
    data = execmany(q,inputs).fetchall()
    info=[]
    temp=[]
    if data is None:
        return info
    for value in data:
        for cell in value:
            temp.append(cell)
        info.append(temp)
    return info

def getBuddy(osis):
    q="SELECT buddy FROM user_tbl WHERE osis=?"
    inputs(osis,)
    buddy = execmany(q,inputs).fetchone()[0]
    q="SELECT * FROM transaction_tbl WHERE recipient=?"
    inputs = (buddy,)
    data=execmany(q,inputs).fetchone()
    info=[]
    if data is None:
        return info
    for value in data:
        info.append(value)
    return info
