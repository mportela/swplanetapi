import json
import app
import unittest
from flask_pymongo import PyMongo


class SWAPITestCase(unittest.TestCase):

    def _clear_data(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            for p in planet.find():
                planet.delete_one({'_id': p['_id']})

    def setUp(self):
        app.app.config['MONGO_DBNAME'] = 'unittestdb'
        # meu docker-compose fornece o servico mongodb com nome mongodb
        app.app.config['MONGO_URI'] = 'mongodb://mongodb:27017/unittestdb'
        app.app.testing = True
        if not hasattr(app, 'mongo'):
            app.mongo = PyMongo(app.app)
        self.app = app.app.test_client()
        self.ac = app.app
        self.mongo = app.mongo

    def test_get_empty_db(self):
        ret = self.app.get('/planet')
        ret = json.loads(ret.data)
        self.assertEqual(ret['result'], [])

    def test_get_all(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            planet_1 = planet.insert({'nome': 'teste1',
                                      'terreno': 'acidentado',
                                      'clima': 'frio', 'filmes': 0})
            planet_2 = planet.insert({'nome': 'teste planeta espécial',
                                      'terreno': 'liso',
                                      'clima': 'quente', 'filmes': 0})

        ret = self.app.get('/planet')
        ret = json.loads(ret.data)
        exp_ret = [
                {'_id': str(planet_1),
                 'clima': 'frio',
                 'filmes': 0,
                 'nome': 'teste1',
                 'terreno': 'acidentado'},
                {'_id': str(planet_2),
                 'clima': 'quente',
                 'filmes': 0,
                 'nome': 'teste planeta espécial',
                 'terreno': 'liso'}
        ]
        self.assertEqual(ret['result'], exp_ret)

    def tearDown(self):
        self._clear_data()


if __name__ == '__main__':
    unittest.main()
