# -*- coding: utf-8 -*-
"""
db.model is a thin layer over MongoDB python driver (pymongo).
Its provides some syntatic-sugar for avoiding common mistakes like typos on
collection names and so.
All classes which inherits from `Model` should easily access the underlying
pymongo's bare Collection. Its does so via the `collection` attribute.
It also provide some methods to ensure validations, structure
(not obstrusively, i.e., you can have extra parameters aside from the
strucuture, this makes sense since we are dealing with a schemaless DB), and
simple queries.

"""
import pymongo
import logging
from copy import deepcopy

logging.basicConfig(level=logging.DEBUG)


# internal set for registering subclasses of Model
_models_registry = set()


def connect(config):
    """
    This method is used to automatically connect all registered sub-classes
    from Model to a proper mongodb connection.


    Parameters:
      :config: a config class with MONGO_DBNAME or
               a config class with `.get_db()` method or
               a string with database_name

    """
    for model in _models_registry:
        model.connect(config)


class ModelMCS(type):
    def __new__(mcs, name, bases, attrs):
        new_cls = super(ModelMCS, mcs).__new__(mcs, name, bases, attrs)
        if name != 'Model':
            _models_registry.add(new_cls)
        return new_cls


class ModelCursor(object):
    """
    ModelCursor is a simple wrapper over `pymongo.cursor.Cursor`.
    Its used internally on Model queries (and should be only used internally).

    All it does is, for some special query methods in the model, delegate to
    pymongo's cursor and wrapps the returned dict into a model instance or
    enable chaining methods.

    Methods:
      :find:  delegates a query to mongodb.

      :first:  used to retrieve the first result from a query result.

      :count:  return the number of result for the query

    """

    def __init__(self, model, *a, **kw):
        self.model = model

    def __iter__(self):
        return self

    def next(self):
        out = self.mongo_cursor.next()
        return self.model(out)

    def find(self, *args, **kwargs):
        """
        Makes a `.find()` on mongoDB with the very same parameters as pymongo
        Returns itself for chaining with other calls.

        For more info on parameters see:
        http://api.mongodb.org/python/current/api/pymongo/collection.html

        """
        self.mongo_cursor = pymongo.cursor.Cursor(self.model.collection,
                                                  *args, **kwargs)
        return self

    def first(self):
        """
        returns a model instance to the first result from the
        query (made before)
        """
        out = self.mongo_cursor[0]
        return self.model(out)

    def count(self):
        """ returns the query results count. """
        return self.mongo_cursor.count()


class Model(object):
    """
    This class should be inherited from all your models.
    It must have a `collection_name` class attribute with a string containing
    the name of the collection.

    """
    __metaclass__ = ModelMCS

    collection = None

    @classmethod
    def connect(cls, db_conf):
        """
        This method connects the model to the database and instantiate the
        `collection` class attribute with a `pymongo.collection.Collection`
        given the `collection_name`

        Parameters:
          :db_conf:  a config class with MONGO_DBNAME or
                     a config class with `.get_db()` method or
                    a string with database_name

        """
        if not cls.collection_name:
            raise Exception('You must provide a collection name')

        if isinstance(db_conf, (str, unicode)):
            logging.debug('setting db from str/unicode')
            _cx = pymongo.Connection(safe=True, max_pool_size=20)
            _db = _cx[db_conf]
            cls.collection = _db[cls.collection_name]

        elif hasattr(db_conf, 'get_db'):
            logging.debug('Setting db from config.get_db')
            cls.collection = db_conf.get_db()[cls.collection_name]
        elif hasattr(db_conf, 'MONGO_DBNAME'):
            logging.debug('setting db from config.MONGO_DBNAME')
            _cx = pymongo.Connection(safe=True, max_pool_size=20)
            _db = _cx[db_conf.MONGO_DBNAME]
            cls.collection = _db[cls.collection_name]
        else:
            raise Exception('Could not set database properly')

    def __init__(self, *args, **kw):
        """
        The model constructor accepts data form a dictionary or any number of
        keyword arguments.
        It builds an internal data dict `_data` which holds all attributes.

        examples:
        ```
            model = MyModel({'a': 1, 'b': 2})
            model = MyModel(a=1, b=2)
            model = MyModel({'a': 1}, b=2)
            # they all build the same data atributes.
        ```
        """
        self._data = {}
        if len(args) > 0 and isinstance(args[0], dict):
            for field, value in args[0].iteritems():
                self._data[field] = value
                setattr(self, field, value)
        if kw:
            for field, value in kw.iteritems():
                if 'data' in kw.keys():
                    raise NameError(
                        'The attribute \'data\' is reserved for this class!')
                self._data[field] = value
                setattr(self, field, value)

    def __setattr__(self, name, value):
        # Override set to send any new values to data dict
        if not hasattr(self, '_data'):
            object.__setattr__(self, '_data', {})
        if name != 'data':
            self._data[name] = value
            object.__setattr__(self, name, value)
        else:
            self._set_data(value)

    def _get_data(self):
        # .data getter property. See more on the pydoc below
        return self._data

    def _set_data(self, new_data):
        # .data setter property. See more on the pydoc below
        if isinstance(new_data, dict) and new_data:
            self._data = deepcopy(new_data)
            for field, value in self._data.iteritems():
                object.__setattr__(self, field, value)

    """
    The data property works like a simple proxy for getter, but on setter it
    makes a partial update, i.e., it merges the new dict with the old one,
    the new attributes gets added, the existing ones get updates, any attribute
    non-presente on the new dict stays untouched.
    """
    data = property(_get_data, _set_data)

    def upsert(self):
        """
        Method for inserting and updating a documment.
        If your class don't have an `_id` property it inserts a new record on
        the collection and automatically set the `_id` attribute on the model.
        In the other case, where you have an _id property it will make a
        **partial** update,i.e., intead of replacing the document it will only
        update the document with the `data` property fields.
        """
        if getattr(self, '_id', None):
            # TODO: use to_dict instead of self.data
            data_ = deepcopy(self.data)
            if '_id' in data_:
                del data_['_id']
            r = self.collection.update(
                {'_id': self._id},
                {'$set': data_},
                safe=True)
        else:
            r = self.collection.insert(self.data)
            self._id = r
        return r

