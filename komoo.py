#! /usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from flask import g, Flask
from settings import config
from main.views import app as main_bp


class Komoo(object):
    """
    This class is a container for our Flask app which configures all the
    necessary behavior and register all the blueprints.

    All our views should belong to a blueprint and the blueprints mounted on
    the main App.

    To run our application you need only to instantiate this class, given a
    config object, and call its run method.

    example:
        ```
        app = Komoo(my_config_obj)
        app.run()
        ```
    """

    # tuples with the blueprint and the url prefix
    blueprints = [
        (main_bp, '/'),
    ]

    def __init__(self, config):
        self.config = config

        self.app = Flask('komoo')
        self.app.config.from_object(config)

        self.db = config.get_db()


        # flush pending mongodb requests
        def call_end_request(response):
            self.db.connection.end_request()
            return response

        # makes possible to access the db directly from any view 
        # (possible, but **not encouraged**, avoid doing this)
        def add_db_to_request():
            g.db = self.db

        self.app.before_request(add_db_to_request)
        self.app.after_request(call_end_request)

        # register all blueprints
        self.register_blueprints()

    def register_blueprints(self):
        for bp in self.blueprints:
            self.app.register_blueprint(bp[0], url_prefix=bp[1])

    def run(self):
        """run Forest, ruuunnnn!"""
        self.app.run()

if __name__ == '__main__':
    komoo = Komoo(config)
    komoo.run()


