# -*- coding: utf-8 -*-
import pymongo

_models_registry = set()


def connect(config):
    for model in _models_registry:
        model.connect(config)


class ModelMCS(type):
    def __new__(mcs, name, bases, attrs):
        new_cls = super(ModelMCS, mcs).__new__(mcs, name, bases, attrs)
        if name != 'Model':
            _models_registry.add(new_cls)
        return new_cls


class ModelCursor(object):

    def __init__(self, model, *a, **kw):
        self.model = model
        self.mongo_cursor = pymongo.cursor.Cursor(model.collection, *a, **kw)

    def __iter__(self):
        return self

    def next(self):
        out = self.mongo_cursor.next()
        return self.model(out)

    def first(self):
        out = self.mongo_cursor[0]
        return self.model(out)

