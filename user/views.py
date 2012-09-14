# -*- coding: utf-8 -*-
import requests
from werkzeug.urls import Href, url_decode
from string import letters, digits
from random import choice

from flask import Blueprint
from flask import request, session
from flask import render_template
from flask import url_for, redirect
from flask import abort

from flask.ext.login import LoginManager
from flask.ext.login import login_required, login_user

from .models import User

app = Blueprint('user', 'user')


def randstr(l=10):
    chars = letters + digits
    s = ''
    for i in range(l):
        s = s + choice(chars)
    return s


########## FLASK LOGIN ##########
@app.route('/login/')
def login():
    return render_template('user/login.html')

login_manager = LoginManager()
login_manager.login_view = 'user.login'  # redirect if not logged in

# append Flask-Login functionality to komoo app
def append_login_manager(state):
    app = state.app
    login_manager.setup_app(app)
app.record(append_login_manager)

@login_manager.user_loader
def load_user(userid):
    # user = User.get(userid)
    user = User()
    return user
#################################


########## FABEBOOK LOGIN ##########
'''INFO: https://developers.facebook.com/docs/authentication/server-side/'''
FACEBOOK_APP_ID = '186391648162058'
FACEBOOK_APP_SECRET = 'd6855cacdb51225519e8aa941cf7cfee'

@app.route('/login/facebook/')
def login_facebook():
    href = Href('https://www.facebook.com/dialog/oauth')
    csrf_token = randstr(10)
    params = {
        # client_id: app id from provider.
        # redirect_uri: where the user will be redirected to.
        # scope: comma separated list of requested permissions.
        # state: some arbitrary but unique string. Used to prevent from CSRF.
        'client_id': FACEBOOK_APP_ID,
        'redirect_uri': url_for('user.facebook_authorized', _external=True),
        'scope': 'email',
        'state': csrf_token,
    }
    session['state'] = csrf_token
    href = href(**params)
    return redirect(href)

@app.route('/login/facebook/authorized/')
def facebook_authorized():
    csrf_token = request.args.get('state', None)
    if not csrf_token or csrf_token != session['state']:
        abort(403)  # csrf attack! get that bastard!

    error = request.args.get('error', None)
    if error:
        error_description = request.args.get('error_description', None)
        return render_template("user/login.html", error_msg=error_description)

    href = Href('https://graph.facebook.com/oauth/access_token')
    params = {
        # client_id: app id from provider.
        # client_secret: app secret from provider.
        # code: code given by provider to exchange for an access_token.
        # redirect_uri: must be the same as the one in step 1.
        'client_id': FACEBOOK_APP_ID,
        'client_secret': FACEBOOK_APP_SECRET,
        'code': request.args.get('code'),
        'redirect_uri': url_for('user.facebook_authorized', _external=True),
    }
    href = href(**params)
    data = url_decode(requests.get(href).content)
    access_token = data['access_token']

    href = Href('https://graph.facebook.com/')
    href = href('me', fields='email,name', access_token=access_token)
    
    # TODO: create user using name and email
    # TODO: persist access_token and expiration in DB

    user = User()
    login_user(user)
    
    return redirect(url_for('user.secret'))

####################################


########## GOOGLE LOGIN ##########
'''INFO: 

STEP 1 - Getting authorization from the user
  https://developers.google.com/accounts/docs/OAuth2Login

STEP 2 - Exchange the authorization code for an access_token
  https://developers.google.com/accounts/docs/OAuth2WebServer

STEP 3 - Accessing the API
'''
GOOGLE_APP_ID = '806210666216.apps.googleusercontent.com'
GOOGLE_APP_SECRET = 'wWFaxUXs3C7atzHThA-YD8T3'

@app.route('/login/google/')
def login_google():
    href = Href('https://accounts.google.com/o/oauth2/auth')
    csrf_token = randstr(10)
    params = {
        # client_id: app id from google.
        # redirect_uri: where the user will be redirected to.
        # scope: space separated list of requested permissions.
        # state: some arbitrary but unique string. Used to prevent from CSRF.
        # response_type: 'code' or 'token', depends on the application type.
        'client_id': GOOGLE_APP_ID,
        'redirect_uri': url_for('user.google_authorized', _external=True),
        'scope': 'https://www.googleapis.com/auth/userinfo.profile '  # space separated
                 'https://www.googleapis.com/auth/userinfo.email',
        'state': csrf_token,
        'response_type': 'code'
    }
    session['state'] = csrf_token
    href = href(**params)
    return redirect(href)

@app.route('/login/google/authorized/')
def google_authorized():
    csrf_token = request.args.get('state', None)
    if not csrf_token or csrf_token != session['state']:
        abort(403)  # csrf attack! get that bastard!

    error = request.args.get('error', None)
    if error:
        error_description = request.args.get('error_description', None)
        return render_template("user/login.html", error_msg=error_description)

    href = 'https://accounts.google.com/o/oauth2/auth'
    params = {
        # client_id: app id from provider.
        # client_secret: app secret from provider.
        # code: code given by provider to exchange for an access_token.
        # redirect_uri: must be the same as the one in step 1.
        # grant_type: just to meet the OAuth 2.0 specification.
        'client_id': GOOGLE_APP_ID,
        'client_secret': GOOGLE_APP_SECRET,
        'code': request.args.get('code'),
        'redirect_uri': url_for('user.google_authorized', _external=True),
        'grant_type': 'authorization_code'
    }
    return requests.post(href, data=params).content  # google requires POST, not GET
    


##################################


@app.route('/secret/')
@login_required
def secret():
    return render_template('user/secret.html')
