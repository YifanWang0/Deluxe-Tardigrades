import sqlite3
from utl.db_builder import exec, execmany
import sys
import random
from datetime import datetime
from datetime import timedelta

def userValid(osis,password):
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

def addUser(osis, password, grade, buddy, survey, locker, gender):
    q = "SELECT * FROM user_tbl WHERE osis=?"
    inputs = (osis,)
    data = execmany(q, inputs).fetchone()
    if (data is None):
        q = "INSERT INTO user_tbl VALUES(?, ?, ?, ?, ?, ?, ?)"
        inputs = (osis, password)
        execmany(q, inputs)
        return True
    return False
