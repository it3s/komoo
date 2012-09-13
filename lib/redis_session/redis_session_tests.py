# -*- coding: utf-8 -*-
import unittest
from flask import Flask, session, request
from redis_session import RedisSessionInterface, RedisSession


class RedisSessionTests(unittest.TestCase):

    def setUp(self):
        app = Flask('redis_sesion_test')
        app.secret_key = 'testkey'
        app.session_interface = RedisSessionInterface()
        app.config['TESTING'] = True

        @app.route('/set', methods=['POST'])
        def set():
            self.assertIn('RedisSession', repr(session))
            session['value'] = request.form['value']
            return 'value set'

        @app.route('/get')
        def get():
            return session['value']

        self.app = app

    def test_session_interface(self):
        self.assertIs(
                self.app.session_interface.session_class,
                RedisSession)

        c = self.app.test_client()
        self.assertEqual(
                c.post('/set', data={'value': '42'}).data,
                'value set')
        self.assertEqual(
                c.get('/get').data,
                '42')

if __name__ == '__main__':
    unittest.main()

