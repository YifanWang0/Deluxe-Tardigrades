import sqlite3

DB_FILE = "locker.db"

#==========================================================
# EXEC COMMANDS

def exec(cmd):
    '''def exec(cmd): Executes a sqlite command'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    output = c.execute(cmd)
    db.commit()
    return output

def execmany(cmd, inputs):
    '''def execmany(cmd, inputs): Executes a sqlite command using ? placeholder'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    output = c.execute(cmd, inputs)
    db.commit()
    return output

#==========================================================
# BUILD DATABASE WITH ALL NECESSARY TABLES

def build_db():
    '''def build_db(): Creates database if it does not yet exist with the necessary tables'''
    command = "CREATE TABLE IF NOT EXISTS user_tbl (osis INT, password TEXT, locker INT, grade INT, buddy INT, survey TEXT, history TEXT)"
    exec(command)

    command = "CREATE TABLE IF NOT EXISTS locker_tbl (locker INT, owner TEXT, combo TEXT, floor INT, level INT, location TEXT, status TEXT)"
    exec(command)

    command = "CREATE TABLE IF NOT EXISTS transaction_tbl (id INT, locker INT, to INT, from INT, status TEXT, request INT)"
    exec(command)
