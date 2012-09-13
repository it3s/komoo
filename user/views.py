# -*- coding: utf-8 -*-
import requests
from flask import Blueprint, render_template
from flask import url_for, redirect
from werkzeug.urls import Href

app = Blueprint('user', 'user')


@app.route('/login/')
def login():
    return render_template('user/login.html')

########## FABEBOOK LOGIN ##########
'''INFO: https://developers.facebook.com/docs/authentication/server-side/'''

@app.route('/login/facebook')
def login_facebook():
    href = Href('https://www.facebook.com/dialog/oauth')
    params = {
        # client_id: app id from facebook
        'client_id': '186391648162058',
        # redirect_uri: where the user will be redirected to
        'redirect_uri': url_for('user.facebook_authorized', _external=True),
        # scope: comma separated list of requested permissions
        'scope': 'email',
        # state: some arbitrary but unique string. Used to prevent from CSRF.
        'state': 'lalala',
    }
    href = href(**params)
    return redirect(href)

@app.route('/login/facebook/authorized')
def facebook_authorized():
    return "facebook authorized!"

####################################
