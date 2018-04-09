import json
import app
import unittest
from flask_pymongo import PyMongo


class SWAPITestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['MONGO_DBNAME'] = 'unittestdb'
        app.app.config['MONGO_URI'] = 'mongodb://mongodb:27017/unittestdb'
        app.app.testing = True
        app.mongo = PyMongo(app.app)
        self.app = app.app.test_client()

    def test_get_empty_db(self):
        ret = self.app.get('/planet')
        ret = json.loads(ret.data)
        self.assertEqual(ret['result'], [])

if __name__ == '__main__':
    unittest.main()
