# -*- coding: utf-8 -*-
import unittest
import pymongo


def _get_test_db():
    # TODO use proper settings for this
    db_name = 'komoo_test'
    cx = pymongo.Connection()
    cx.drop_database(db_name)
    db = cx[db_name]
    return db


class Counter:
    # utility class to use with connexions testing
    num = 0

    @classmethod
    def inc(cls):
        cls.num += 1

    @classmethod
    def ensure_0(cls):
        cls.num = 0


class CounterTest(unittest.TestCase):
    # test the utility test class -> TestInception
    def setUp(self):
        self.counter = Counter()
        self.counter.ensure_0()

    def tearDown(self):
        del self.counter

    def test_counter_creation(self):
        self.assertEqual(self.counter.num, 0)

    def test_counter_inc(self):
        self.counter.inc()
        self.assertEqual(self.counter.num, 1)

    def test_multiple(self):
        counter1 = Counter()
        counter2 = Counter()
        Counter.ensure_0()
        counter1.inc()
        counter2.inc()
        self.assertEqual(counter1.num, counter2.num)
        self.assertEqual(Counter.num, 2)
        del counter1
        del counter2


class ModelModuleTests(unittest.TestCase):

    def test_connect(self):
        import model

        connexions = Counter()
        Counter.ensure_0()
        config = type('ConfigMock', (), {})()

        # mocking a model
        DummyModel = type('ModelMock', (), {})

        def mocked_connect(test):
            def _connect(conf):
                connexions.inc()
                test.assertIs(conf, config)
            return _connect

        model1 = DummyModel()
        model1.connect = mocked_connect(self)

        model2 = DummyModel()
        model2.connect = mocked_connect(self)

        model._models_registry = set([model1, model2])
        model.connect(config)
        self.assertEqual(connexions.num, 2)


class MetaModelTests(unittest.TestCase):
    def test_model_registration(self):
        import model
        from model import ModelMCS

        class Model(object):
            __metaclass__ = ModelMCS

        class NewModel(Model):
            pass

        # only NewModel should be registered
        self.assertEqual(len(model._models_registry), 1)

        self.assertEqual(list(model._models_registry)[0], NewModel)
        self.assertEqual(NewModel.__metaclass__, ModelMCS)

        class AnotherModel(Model):
            pass

        self.assertEqual(len(model._models_registry), 2)


class ModelCursorTests(unittest.TestCase):
    db = _get_test_db()

    def setUp(self):
        from model import ModelCursor
        collection = self.db.cursor_test

        class ModelMock:
            def __init__(self, *a, **kw):
                if len(a) > 0 and isinstance(a[0], dict):
                    self.obj = a[0]
                else:
                    self.obj = None

        self.ModelMock = ModelMock
        ModelMock.collection = collection
        self.model = ModelMock()

        self.cursor = ModelCursor(self.model.__class__)

    def tearDown(self):
        self.db.drop_collection('cursor_test')

    def test_pymongo_cursor_wrapping(self):
        assert isinstance(self.cursor.find().mongo_cursor,
                    pymongo.cursor.Cursor)

    def test_cursor_next_returns_model_instance(self):
        self.model.collection.save({'name': 'model1'})

        self.assertEqual(self.cursor.find().next().__class__,
                self.model.__class__)

    def test_iteration_returns_model_instance(self):
        dict1 = {'name': 'model1'}
        dict2 = {'name': 'model2'}
        self.model.collection.save(dict1)
        self.model.collection.save(dict2)

        for m in self.cursor.find():
            assert isinstance(m, self.ModelMock)

    def test_first_return_0_index_value_from_find(self):
        dict1 = {'name': 'model1'}
        dict2 = {'name': 'model2'}
        self.model.collection.save(dict1)
        self.model.collection.save(dict2)

        assert isinstance(self.cursor.find().first(), self.ModelMock)
        self.assertEqual(self.cursor.find().first().obj['name'], dict1['name'])

    def test_find(self):
        model_dict = {'name': 'find test'}
        self.model.collection.save(model_dict)

        assert isinstance(
                self.cursor.find({'name': 'find test'}).next(),
                self.model.__class__)

        self.assertEqual(
                self.cursor.find({'name': 'find test'}).first().obj['name'],
                model_dict['name'])

    def test_count(self):
        model_dict = {'name': 'find test'}
        self.model.collection.save(model_dict)

        self.assertEqual(
                self.cursor.find({'name': 'find test'}).count(), 1)


# class ModelTests(unittest.TestCase):
#     def test_connect_from_str(self):
#         # TODO use settings
#         db_conf = 'db_name'
#
#     def test_connect_from_class(self):
#         class conf(object):
#             MONGO_DBNAME = 'db_name'
#
#         db_conf = conf
#
#     def test_connect_from_method(self):
#         class conf(object):
#             @classmethod
#             def get_db(cls):
#                 return _get_test_db()
#
#         db_conf = conf


if __name__ == '__main__':
    unittest.main()

