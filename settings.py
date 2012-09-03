# -*- coding: utf-8 -*-
import os
import pymongo


class Config:
    DEBUG = False
    SECRET_KEY = 'blabalblaeuamobatatinhafritacomcocacolablabalbba'
    MONGO_DBNAME = 'komoo_db'

    _db = None

    @classmethod
    def get_db(cls):
        """returns always the same connection pool instance"""
        mongo_db = cls._db
        if not cls._db:
            mongo_cx = pymongo.Connection(safe=True, max_pool_size=10)
            mongo_db = mongo_cx[cls.MONGO_DBNAME]
            cls._db = mongo_db
        return mongo_db


class Development(Config):
    DEBUG = True
    MONGO_DBNAME = 'komoo_dev'


class Staging(Config):
    MONGO_DBNAME = 'komoo_stage'


class Testing(Config):
    MONGO_DBNAME = 'komoo_test'
    TESTING = True
    DEBUG = True


class Production(Config):
    pass


configs = {
    'dev': Development,
    'stage': Staging,
    'prod': Production,
}

# We expect a environment variable KOMOO_CONFIG to tell us
# which config to use
env_ = os.environ.get('KOMOO_CONFIG', 'dev')

config = configs[env_]


