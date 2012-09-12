import unittest
from komoo import create_app
from settings import Testing


class KomooInstanceTest(unittest.TestCase):
    def test_instantiate_app(self):
        komoo_app = create_app(Testing)
        self.assertTrue(komoo_app)
        self.assertTrue(hasattr(komoo_app, 'run'))

        app = komoo_app.test_client()
        self.assertTrue(app)

if __name__ == '__main__':
    unittest.main()
