# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

app = Blueprint('user', 'user')


@app.route('/login/')
def login():
    return render_template('user/login.html')

########## FABEBOOK LOGIN ##########
@app.route('/login/facebook')
def login_facebook():
    return "LALALA"

####################################
