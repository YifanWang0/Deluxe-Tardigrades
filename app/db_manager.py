import sqlite3
from db_builder import exec, execmany
import sys
import random
from datetime import datetime
from datetime import timedelta

def userValid(osis,password):
    q = "SELECT * FROM user_tbl"
    data = exec(q)
    for uName in data:
        if uName[0] == osis:
            q = "SELECT password from user_tbl WHERE osis=?"
            inputs = (osis,)
            data = execmany(q, inputs)
            for passW in data:
                if (passW[0] == password):
                    return True
    return False

def addUser(osis, password, grade, buddy, survey, locker, gender,locker_info):
    q = "SELECT * FROM user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    if (data is None):
        q = "SELECT * FROM locker_tbl WHERE locker=?"
        inputs = (locker,)
        data = execmany(q, inputs).fetchone()
        if(data is None):
            q = "INSERT INTO user_tbl VALUES(?, ?, ?, ?, ?, ?)"
            inputs = (osis, password, locker, grade, buddy, survey)
            execmany(q, inputs)
            q = "INSERT INTO locker_tbl VALUES(?, ?, ?, ?, ?, ?, ?)"
            inputs = (locker, osis, locker_info[0], locker_info[1], locker_info[2], locker_info[3], locker_info[4])
            execmany(q, inputs)
            return "done"
        else:
            "locker"
    return "user"
