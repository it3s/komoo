import unittest
from komoo import Komoo
from settings import Testing
import pymongo


class KomooInstanceTest(unittest.TestCase):
    def test_instantiate_app(self):
        komoo = Komoo(Testing)
        self.assertTrue(komoo)
        self.assertTrue(hasattr(komoo, 'run'))

        self.assertEqual(komoo.config, Testing)
        self.assertTrue(hasattr(komoo, 'blueprints'))
        self.assertTrue(len(komoo.blueprints) > 0)

        self.assertTrue(komoo.db)
        self.assertIsInstance(komoo.db.connection, pymongo.Connection)

        app = komoo.app.test_client()
        self.assertTrue(app)

if __name__ == '__main__':
    unittest.main()
