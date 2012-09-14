# -*- coding: utf-8 -*-
import unittest
from komoo import create_app
from settings import Testing


class LoginTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(Testing)
        cls.client = cls.app.test_client()

    def test_login_page(self):
        resp = self.client.get('/login/')
        self.assertTrue(resp)
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
