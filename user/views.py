# -*- coding: utf-8 -*-
import requests
from werkzeug.urls import Href, url_decode

from flask import Blueprint
from flask import request
from flask import render_template
from flask import url_for, redirect

app = Blueprint('user', 'user')


@app.route('/login/')
def login():
    return render_template('user/login.html')

########## FABEBOOK LOGIN ##########
'''INFO: https://developers.facebook.com/docs/authentication/server-side/'''
FACEBOOK_APP_ID = '186391648162058'
FACEBOOK_APP_SECRET = 'd6855cacdb51225519e8aa941cf7cfee'

@app.route('/login/facebook')
def login_facebook():
    href = Href('https://www.facebook.com/dialog/oauth')
    params = {
        # client_id: app id from facebook
        # redirect_uri: where the user will be redirected to
        # scope: comma separated list of requested permissions
        # state: some arbitrary but unique string. Used to prevent from CSRF.
        'client_id': FACEBOOK_APP_ID,
        'redirect_uri': url_for('user.facebook_authorized', _external=True),
        'scope': 'email',
        'state': 'abebubaba',  # TODO: randomize and save state in session
    }
    href = href(**params)
    return redirect(href)

@app.route('/login/facebook/authorized')
def facebook_authorized():
    # TODO: verifiy request.args.get('state') saved in session
    href = Href('https://graph.facebook.com/oauth/access_token')
    params = {
        # client_id: app id from facebook
        # client_secret: app secret from facebook
        # code: code given by facebook to exchange for an access_token
        # redirect_uri: must be the same as the one in the login_facebook
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
    
    return requests.get(href).content
    return render_template('home.html', email=)

####################################
