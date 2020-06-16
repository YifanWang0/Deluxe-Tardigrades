import sqlite3
from db_builder import exec, execmany
import sys
import random
from datetime import datetime
from datetime import timedelta
from flask import flash

#==========================general data retrieval functions===========================

# returns user info in a list given an osis
def getUserInfo(osis):
    q = "SELECT * from user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    info = [data[0],data[1],data[2],data[3],data[4],data[5],data[6]]
    return info

# returns locker info in a list given an osis and locker
def getLockerInfo(locker,osis):
    q = "SELECT * from locker_tbl WHERE locker=? AND owner = ?"
    inputs = (locker,osis)
    data = execmany(q, inputs).fetchone()
    info=[]
    if data is not None:
        for value in data:
            info.append(value)
    return info

# returns transaction info in a list given an osis
def getTransactionInfo(osis):
    q = "SELECT * from transaction_tbl WHERE sender=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchall()
    info = []
    if(data is None):
        return info
    for value in data:
        if len(value)>0 and value[3] == 1:
            info.append([value[0],value[1],value[2],value[3],value[4],value[5]])
    return info

# returns a list of all info from a desired column of a desired table
def getColumnInfo(column, table):
    q = "SELECT " + column + " FROM " + table + "_tbl"
    rawData = exec(q).fetchall()
    info = []
    for entry in rawData:
        info.append(entry[0])
    return info

# returns a list of info from a desired column of a desired table given specific requirements
def getColumnInfo_Specific(column, table, requirement):
    q = "SELECT " + column + " FROM " + table + "_tbl WHERE " + requirement
    rawData = exec(q).fetchall()
    info = []
    for entry in rawData:
        info.append(entry[0])
    return info

# finds a specific osis from user_tbl and returns True if it exists
def findOsis(osis):
    q = "SELECT * FROM user_tbl WHERE osis = ?"
    inputs=(osis,)
    data=execmany(q,inputs).fetchall()
    if len(data) != 0:
        return True
    return False

# creates dict of transaction/locker data given list of tuples
def getTransLock(data,osis):
    dataDict = {}
    for i in data:
        lock = getLockerInfo(i[0],osis)
        dataDict[i] = lock
    return dataDict

# returns a list of all people who the user received a transaction request from
def getTransactionFrom(osis):
    q="SELECT recipient FROM transaction_tbl WHERE sender=? AND status = ?"
    inputs = (osis,1)
    data = execmany(q,inputs).fetchall()
    info=[]
    if data is None:
        return info
    for value in data:
        info.append(value[0])
    filtered = [x for x in info if x != '']
    return filtered

# returns a list of all people who the user sent a transaction request to
def getTransactionTo(osis):
    q="SELECT sender FROM transaction_tbl WHERE recipient=? AND status=?"
    inputs = (osis,1)
    data = execmany(q,inputs).fetchall()
    info=[]
    if data is None:
        return info
    for value in data:
        info.append(value[0])
    return info

#==========================user profile functions===========================

# checks to see if the user/password combination is valid
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

# adds user info to user_tbl and locker info to locker_tbl
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

#==========================editing functions===========================

# updates the survey column of user_tbl given an osis and the proper info
def updateSurvey(osis, info):
    q = "UPDATE user_tbl SET survey=? WHERE osis=?"
    inputs = (info, osis)
    execmany(q, inputs)

# edits user_tbl given an osis, the desired column to be changed, and the new info
def editUserTbl(osis,fxn,new):
    new = "\"" + new + "\""
    q = "UPDATE user_tbl SET " + fxn + "=" + new + " WHERE osis=?"
    inputs = (osis,)
    data = execmany(q,inputs)
    return True

# edits transaction_tbl given an osis, the desired column to be changed, and the new info
def editTransTbl(osis,fxn,new):
    if fxn == "locker":
        q="UPDATE transaction_tbl SET locker = ? WHERE recipient = ?"
        inputs = (new,osis)
        execmany(q,inputs)
    else:
        q = "UPDATE transaction_tbl SET sender = ? WHERE sender = ?"
        inputs = (new, osis)
        execmany(q,inputs)
        q = "UPDATE transaction_tbl SET recipient = ? WHERE recipient = ?"
        inputs = (new, osis)
        execmany(q,inputs)
    return True

# edits locker_tbl given an osis, the locker, the desired column to be changed, and the new info
def editLockerTbl(locker,fxn,new, osis):
    if fxn == "locker" or fxn == "floor":
        q="SELECT locker, floor FROM locker_tbl WHERE locker = ?"
        inputs=(locker,)
        old = execmany(q,inputs).fetchone()
        if fxn == "locker":
            q = "SELECT locker, floor FROM locker_tbl WHERE locker = ?"
            inputs=(new,)
            data = execmany(q,inputs).fetchall()
        else:
            q = "SELECT locker, floor FROM locker_tbl WHERE floor = ?"
            inputs=(new,)
            data = execmany(q,inputs).fetchall()
        if data is not None:
            for value in data:
                if value[0] == old[0] and value[1] == old[1]:
                    return False
    new = "\"" + new + "\""
    q = "UPDATE locker_tbl SET " + fxn + "=" + new + " WHERE owner=?"
    inputs = (osis,)
    d= execmany(q, inputs)
    q= "SELECT floor FROM locker_tbl WHERE owner = ? AND locker = ?"
    inputs = (osis, locker)
    d= execmany(q,inputs).fetchone()
    if d is not None:
        q = "UPDATE transaction_tbl SET floor = ? WHERE locker=? AND floor = ?"
        inputs = (new, locker, d[0])
        data = execmany(q,inputs)
    else:
        q = "UPDATE transaction_tbl SET floor = ? WHERE locker=?"
        inputs = (new, locker)
        data = execmany(q,inputs)
    return True

# edits user/locker/transaction_tbl depending on the new information provided by the user
def editUser(oldosis, osis, oldpassword, password, grade, locker, gender, combo, floor, level, type):
    bool = True
    if(userValid(oldosis,oldpassword)):
        if (password != ""): editUserTbl(oldosis,"password",password)
        if (grade != ""): editUserTbl(oldosis,"grade", grade)
        if (gender != ""): editUserTbl(oldosis,"gender", gender)
        q = "SELECT locker FROM user_tbl WHERE osis=?"
        inputs = (oldosis,)
        oldlocker = execmany(q,inputs).fetchone()[0]
        if (combo != ""): editLockerTbl(oldlocker,"combo", combo, oldosis)
        if (floor != ""): bool = bool and editLockerTbl(oldlocker,"floor", floor, oldosis)
        if (level != ""): editLockerTbl(oldlocker,"level", level, oldosis)
        if (type != ""): editLockerTbl(oldlocker,"location", type, oldosis)
        # if the user wants to change their owned locker
        if (locker != ""):
            if(editLockerTbl(oldlocker, "locker", locker, oldosis)):
                editUserTbl(oldosis, "locker", locker)
                editTransTbl(oldosis, "locker", locker)
            else:
                bool = False
        # if the user wants to change their osis
        if (osis != ""):
            if not (findOsis(osis)):
                editTransTbl(oldosis,"notifs",osis)
                q = "UPDATE locker_tbl SET owner=? WHERE owner=?"
                inputs = (osis,oldosis)
                data = execmany(q, inputs)
                editUserTbl(oldosis,"osis",osis)
            else:
                bool = False
    return bool

# deletes an entry from transaction_tbl given the user, recipient, and type of request
def deleteTrans(user, recipient, type):
    # if the user wants to take their locker off the market
    if (recipient == "" and type == 'L'):
        q = "UPDATE locker_tbl SET status='OWNED' WHERE owner=" + user
        exec(q)
    q = "DELETE FROM transaction_tbl WHERE sender=? AND recipient=? AND request=?"
    inputs=(user,recipient,type)
    # print(user,recipient,type)
    execmany(q,inputs)
    return True

#==========================locker trading functions===========================

# returns a dict of transaction_tbl tuples and locker_tbl lists of all available lockers
def tradeableLockers():
    q = "SELECT * FROM transaction_tbl WHERE status=1 AND request='L' AND recipient=''"
    data = exec(q).fetchall()
    dataDict = {}
    for i in data:
        q = "SELECT * from locker_tbl WHERE locker=? AND status='TRADING'"
        inputs = (i[0],)
        data = execmany(q, inputs).fetchone()
        info=[]
        for value in data:
            info.append(value)
        dataDict[i] = info
    return dataDict

# returns a dict of transaction_tbl tuple and locker_tbl list of searched locker
def searchLocker(searchBy, query):
    if (searchBy == "Locker Number"):
        if (len(query) != 5):
            return False
        head,space,tail = query.partition("-")
        q = "SELECT * FROM transaction_tbl WHERE recipient='' AND locker=" + tail + " AND floor=" + head
        data = exec(q).fetchall()
        dataDict = {}
        for i in data:
            q = "SELECT * from locker_tbl WHERE locker=? AND floor=?"
            inputs = (tail,head)
            data = execmany(q, inputs).fetchone()
            info=[]
            if data is not None:
                for value in data:
                    info.append(value)
            dataDict[i] = info
        return dataDict
    else:
        if (len(query) != 9):
            return False
        q = "SELECT * FROM transaction_tbl WHERE recipient='' AND sender=" + query
        data = exec(q).fetchall()
        return getTransLock(data,query)

# searches for all lockers that meet the given criteria with possible searches in floor, level, and location of locker
def filterLocker(floor,level,location):
    # filters based on owner
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
        # searches for those specific owners and their lockers
        dictRes.update(searchLocker("Owner", i[0]))
    return dictRes

# adds a locker to transaction_tbl and updates its status
def putOnMarket(locker,osis):
    linfo = getLockerInfo(locker,osis)
    q = "INSERT INTO transaction_tbl VALUES (?,?,?,?,?,?)"
    inputs = (locker,"",linfo[1],1,'L',linfo[3])
    execmany(q,inputs)
    q = "UPDATE locker_tbl SET status='TRADING' WHERE locker=" + str(locker) + " AND owner=" + str(osis)
    exec(q)

# adds a locker request to transaction_tbl given two people
def lockerRequest(to,sender):
    owner = getUserInfo(to)
    locker = getLockerInfo(owner[2],to)
    q = "INSERT INTO transaction_tbl VALUES (?,?,?,?,?,?)"
    inputs=(owner[2],to, sender, 1, "L", locker[3])
    execmany(q,inputs)

# updates the user/locker/transaction_tbl to switch two lockers for two people
def acceptLocker(me,you):
    owner = getUserInfo(me)
    ownerL = getLockerInfo(owner[2],me)
    recipient = getUserInfo(you)
    recipientL = getLockerInfo(recipient[2],you)
    q = "UPDATE user_tbl SET locker=" + str(recipient[2]) + " WHERE osis=" + str(me)
    exec(q)
    q = "UPDATE user_tbl SET locker=" + str(owner[2]) + " WHERE osis=" + str(you)
    exec(q)
    q = "UPDATE locker_tbl SET status='OWNED',locker=" + str(recipientL[0]) + ",combo=" + str(recipientL[2]) + ",floor=" + str(recipientL[3]) + ",level='" + str(recipientL[4]) + "',location='" + str(recipientL[5]) + "' WHERE owner=" + str(me)
    exec(q)
    q = "UPDATE locker_tbl SET status='OWNED',locker=" + str(ownerL[0]) + ",combo=" + str(ownerL[2]) + ",floor=" + str(ownerL[3]) + ",level='" + str(ownerL[4]) + "',location='" + str(ownerL[5]) + "' WHERE owner=" + str(you)
    exec(q)
    q = "UPDATE transaction_tbl SET status=0 WHERE recipient=" + str(me) + " AND sender=" + str(you)
    exec(q)
    deleteTrans(me,"","L")
    deleteTrans(you,"","L")
    return True

#==========================buddy matching functions===========================

# returns survey info from user_tbl in a list given an osis
def getSurveyInfo(osis):
    q = "SELECT survey from user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    info = []
    if(data[0] != ""):
        info = data[0].split(",")
    return info

# filters the buddy search by using the filterUser and filterLock helper functions, returns a list of osis
def filter(query,osis):
    info1=filterUser(query, osis)
    info2=filterLock(query, osis)
    info=[]
    # intersects the two data sets
    for value in info1:
        if value in info2:
            info.append(value)
    return info

# returns a list of all people who fit query criteria found in user_tbl
def filterUser(query,osis):
    q="SELECT osis FROM user_tbl WHERE osis != " + osis
    q+= " AND BUDDY = ''"
    info=[]
    if query[0] != "":
        q+=" AND osis = '" + query[0]+"'"
    if query[1] != "":
        q+=" AND locker = '" + query[1]+"'"
    if query[2] != "" and  query[2] != "None":
        q+=" AND survey LIKE '%" + query[2] +"%'"
    if query[3] != "" and  query[3] != "None":
        q+=" AND survey LIKE '%" + query[3] +"%'"
    if query[4] != "" and  query[4] != "None":
        q+=" AND grade = '" + query[4]+"'"
    if query[5] != "" and  query[5] != "None":
        q+=" AND gender = '" + query[5]+"'"
        q+=";"
    data=exec(q).fetchall()
    for value in data:
        info.append(str(value[0]))
    return info

# returns a list of all people who fit query criteria found in locker_tbl
def filterLock(query,osis):
    info=[]
    q="SELECT owner FROM locker_tbl WHERE owner != " + osis
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

# adds a buddy request to transaction_tbl
def buddyRequest(to, sender):
    locker = getUserInfo(to)
    if locker == '':
        locker = getUserInfo(sender)[2]
    q = "INSERT INTO transaction_tbl VALUES (?,?,?,?,?,?)"
    inputs=(locker[2],to, sender, 1, "B", getLockerInfo(locker[2],to)[3])
    execmany(q,inputs)
    return True

# confirms a buddy request by updating user_tbl buddy columns for both people
def confirmB(user, recipient):
    q="UPDATE transaction_tbl SET status = 0 WHERE request = ? AND (sender=? OR recipient = ? OR sender = ? OR recipient = ?)"
    inputs=("B",user,user,recipient,recipient)
    execmany(q,inputs)
    q="UPDATE user_tbl SET buddy = ? WHERE osis = ?"
    inputs=(user, recipient)
    execmany(q,inputs)
    q="UPDATE user_tbl SET buddy = ? WHERE osis = ?"
    inputs=(recipient, user)
    execmany(q,inputs)
    return True

# returns a list of senders who want to dissolve a buddy pair with a given user
def getDissolveInfo(user):
    q = "SELECT sender FROM transaction_tbl WHERE recipient=?"
    inputs=(user,)
    data=execmany(q,inputs).fetchall()
    info=[]
    for value in data:
        info.append(value[0])
    return info

# updates user_tbl by removing the buddy pair of two people
def dissolveBuddy(user, sender):
    q = "UPDATE transaction_tbl SET status = ? WHERE (sender = ? OR recipient = ?) AND request = ?"
    inputs=(0,user,user,"D")
    execmany(q,inputs)
    q = "UPDATE user_tbl SET buddy = ? WHERE osis = ?"
    inputs=("",user)
    execmany(q,inputs)
    inputs=("",sender)
    execmany(q,inputs)
    return True

# adds a dissolve buddy request to transaction_tbl
def breakB(user, recipient):
    q = "INSERT INTO transaction_tbl VALUES (?,?,?,?,?,?)"
    inputs=("" , recipient, user, 1, "D", "")
    execmany(q,inputs)
    return True

# searches transaction_tbl to see if a user wants to dissolve a buddy pair
def ifDissolve(user):
    q = "SELECT * FROM transaction_tbl WHERE (recipient=? OR sender=?) AND status = ? AND request = ?"
    inputs=(user,user,1,"D")
    data=execmany(q,inputs).fetchall()
    if len(data)!=0:
        return True
    return False

#==========================notifications functions===========================

# returns a list of transaction requests sent to the user to be displayed as messages
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

# returns a list of all notifications the user was sent
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
