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


# internal set for registering subclasses of Model
_models_registry = set()


def connect(config):
    """
    This method is used to automatically connect all registered sub-classes
    from Model to a proper mongodb connection.


    Parameters:
      :config: a config class, or a database_name

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
        # self.mongo_cursor = pymongo.cursor.Cursor(model.collection, *a, **kw)

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
        """
        returns the query results count.
        """
        return self.mongo_cursor.count()

