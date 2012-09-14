#! /usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from flask import g, Flask, session

from lib.redis_session import RedisSessionInterface

from settings import config
from main.views import app as main_bp
from user.views import app as user_bp


# tuples with the blueprint and the url prefix
blueprints = (
    (main_bp, ''),
    (user_bp, ''),
)


def create_app(config):
    """
    This method is a factory for our Flask app which configures all the
    necessary behavior and register all the blueprints.

    All our views should belong to a blueprint and the blueprints mounted on
    the main App.

    To run our application you need only to instantiate a app using this
    function, given a config object, and call its run method.

    example:

        komoo_app = create_app(my_config_obj)
        komoo_app.run()

    """
    app = Flask('komoo')
    app.config.from_object(config)

    app.session_interface = RedisSessionInterface()

    db = config.get_db()

    def call_end_request(response):
        """
        flush pending mongodb requests
        and return the connection to the poll
        """
        db.connection.end_request()
        return response

    def add_db_to_request():
        """
        makes possible to access the db directly from any view
        (possible, but **not encouraged**, avoid doing this)
        """
        g.db = db

    def permanet_sessions():
        """
        makes the session persistent for
        PERMANENT_SESSION_LIFETIME
        """
        session.permanent = True

    app.before_request(add_db_to_request)
    app.before_request(permanet_sessions)
    app.after_request(call_end_request)

    # register all blueprints
    for bp in blueprints:
        app.register_blueprint(bp[0], url_prefix=bp[1])

    return app


if __name__ == '__main__':
    komoo = create_app(config)
    komoo.run()
