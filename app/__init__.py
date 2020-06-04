# Team Deluxe-Tardigrades :: Yifan Wang, Amber Chen, Elizabeth Doss, Mandy Zheng
# SoftDev pd1
# P05 :: Fin
# 2020-06-11

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import date, timedelta
import db_builder
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

@app.route("/signup")
@no_login_required
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    db_builder.build_db()
    app.debug = True
    app.run()
