# Team Deluxe-Tardigrades :: Yifan Wang, Amber Chen, Elizabeth Doss, Mandy Zheng 
# SoftDev pd1
# P05 :: Fin
# 2020-06-11

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import date, timedelta
from utl.constants import *
import os, random, csv
import urllib3, json, urllib

app = Flask(__name__)

if __name__ == "__main__":
    app.debug = True
    app.run()
