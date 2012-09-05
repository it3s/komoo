# -*- coding: utf-8 -*-
import unittest
import pymongo
import model
from model import ModelMCS, ModelCursor, Model
from settings import Testing


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
        class NewModel(object):
            __metaclass__ = ModelMCS

        # NewModel should be registered
        self.assertEqual(len(model._models_registry), 1)

        self.assertEqual(list(model._models_registry)[0], NewModel)
        self.assertEqual(NewModel.__metaclass__, ModelMCS)

        class AnotherModel(NewModel):
            pass

        self.assertEqual(len(model._models_registry), 2)


class ModelCursorTests(unittest.TestCase):
    db = Testing.get_db()

    def setUp(self):
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
        self.assertIsInstance(self.cursor.find().mongo_cursor,
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
            self.assertIsInstance(m, self.ModelMock)

    def test_first_return_0_index_value_from_find(self):
        dict1 = {'name': 'model1'}
        dict2 = {'name': 'model2'}
        self.model.collection.save(dict1)
        self.model.collection.save(dict2)

        self.assertIsInstance(self.cursor.find().first(), self.ModelMock)
        self.assertEqual(self.cursor.find().first().obj['name'], dict1['name'])

    def test_find(self):
        model_dict = {'name': 'find test'}
        self.model.collection.save(model_dict)

        self.assertIsInstance(
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


class ModelConnectTests(unittest.TestCase):
    def setUp(self):
        class MyModel(Model):
            collection_name = 'model_test'

        self.model = MyModel()

    def test_connect_from_str(self):
        db_conf = Testing.MONGO_DBNAME

        self.assertIs(self.model.collection, None)
        self.model.connect(db_conf)

        self.assertEqual(self.model.collection.name, 'model_test')
        self.assertIsInstance(self.model.collection,
                pymongo.collection.Collection)

    def test_connect_from_class(self):
        class conf(object):
            MONGO_DBNAME = Testing.MONGO_DBNAME

        db_conf = conf
        self.assertIs(self.model.collection, None)
        self.model.connect(db_conf)

        self.assertEqual(self.model.collection.name, 'model_test')
        self.assertIsInstance(self.model.collection,
                pymongo.collection.Collection)

    def test_connect_from_method(self):
        class conf(object):
            @classmethod
            def get_db(cls):
                return Testing.get_db()

        db_conf = conf
        self.assertIs(self.model.collection, None)
        self.model.connect(db_conf)

        self.assertEqual(self.model.collection.name, 'model_test')
        self.assertIsInstance(self.model.collection,
                pymongo.collection.Collection)

    def test_raises_error_when_model_has_no_collection_name(self):
        db_conf = Testing.MONGO_DBNAME

        class WrongModel(Model):
            collection_name = ''
        self.model = WrongModel()

        with self.assertRaises(Exception):
            self.model.connect(db_conf)

    def test_raises_error_when_config_is_not_valid(self):
        db_conf = 986590

        with self.assertRaises(Exception):
            self.model.connect(db_conf)


class ModelInstanceTests(unittest.TestCase):
    def setUp(self):
        class ModelTest(Model):
            collection_name = 'model_test'

        self.ModelTest = ModelTest

    def test_model_instance_empty_data(self):
        model = self.ModelTest()
        self.assertEqual(model._data, {})

    def test_model_instance_dict_data(self):
        data = {'a': 1, 'b': 'bbbbbb'}
        model = self.ModelTest(data)
        self.assertEqual(model._data, data)

    def test_model_instance_kwargs_data(self):
        data = {'a': 1, 'b': 'bbbbbb'}
        model = self.ModelTest(a=1, b='bbbbbb')
        self.assertEqual(model._data, data)

    def test_model_instance_hibrid_data(self):
        data = {'a': 1, 'b': 'bbbbbb'}
        model = self.ModelTest({'a': 1}, b='bbbbbb')
        self.assertEqual(model._data, data)

    def test_model_instace_raises_exception_when_data_on_kwargs(self):
        # regression test
        with self.assertRaises(NameError):
            self.ModelTest(data={'a': 1, 'b': 2})

    def test_model_instance_access_data_from_dot_notation(self):
        model = self.ModelTest({'a': 1}, b='bbbbbb')
        self.assertEqual(model.a, 1)
        self.assertEqual(model.b, 'bbbbbb')

    def test_proxy_setitem_to_data_dict(self):
        model = self.ModelTest(a=1)
        model.b = 2
        model.c = 3
        self.assertEqual(model._data, {'a': 1, 'b': 2, 'c': 3})
        model.c = 4
        self.assertEqual(model._data['c'], 4)

    def test_data_property_getter(self):
        model = self.ModelTest({'a': 1}, b=2)
        model.c = 3
        self.assertEqual(model.data, {'a': 1, 'b': 2, 'c': 3})
        self.assertIs(model.data, model._data)

    def test_data_property_setter(self):
        model = self.ModelTest()
        model.data = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(model.data, {'a': 1, 'b': 2, 'c': 3})
        model.data.update({'a': 2, 'd': 4})
        self.assertEqual(model.data, {'a': 2, 'b': 2, 'c': 3, 'd': 4})


if __name__ == '__main__':
    unittest.main()

