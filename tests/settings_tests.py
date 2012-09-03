# -*- coding: utf-8 -*-
import unittest
from settings import Config, Testing


class SettingsTests(unittest.TestCase):

    def test_config_class(self):
        assert hasattr(Config, 'DEBUG')
        self.assertEqual(Config.DEBUG, False)

        assert hasattr(Config, 'MONGO_DBNAME')
        self.assertEqual(Config.MONGO_DBNAME, 'komoo_db')

    def test_config_override(self):
        assert hasattr(Config, 'DEBUG')
        self.assertEqual(Config.DEBUG, False)

        assert hasattr(Testing, 'DEBUG')
        self.assertEqual(Testing.DEBUG, True)

        self.assertEqual(Config.SECRET_KEY, Testing.SECRET_KEY)

    def test_get_db(self):
        db1 = Testing.get_db()
        assert db1
        self.assertEqual(db1.name, Testing.MONGO_DBNAME)

        db2 = Testing.get_db()

        self.assertIs(db1, db2)



if __name__ == '__main__':
    unittest.main()
