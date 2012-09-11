#! /usr/bin/env python
# -*- coding:utf-8 -*-

##### CONFIG #####
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

class Config(object):
    DEBUG = True
    ASSETS_DEBUG = True

app = Flask(__name__)
app.config.from_object(Config)


##### SESSION CONFIGURATION #####
# set the secret key.  keep this really secret:
app.secret_key = 'jesusismysaviour'


##### LOGIN RELATED #####
from flask.ext.login import LoginManager
from flask.ext.login import login_required, login_user
from flask.ext.login import UserMixin

class User(UserMixin):
    id_ = "m0ng0h4sh"
    
    def get_id(self):
        return unicode(self.id_)

login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    # user = User.get(userid)
    user = User()
    return user


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Page with all login options. A unlogged user should be redirect to this
    page when trying to access a protected resource."""
    if request.method == 'POST':
        print "POSTED"
        if request.form['email'] == "ah.casimiro@gmail.com":
            print "VALIDATED USER"
            user = User()
            login_user(user)
            return redirect("/home")
        else:
            print "WRONG CREDENTIALS"
    return render_template("login.html")


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
