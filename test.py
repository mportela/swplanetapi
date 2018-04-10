import json
import unittest
from unittest.mock import patch
from flask_pymongo import PyMongo

import app


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
        self.planet_cache = app.planet_cache

    def test_get_empty_db(self):
        ret = self.app.get('/planet')
        ret = json.loads(ret.data)
        self.assertEqual(ret['result'], [])
        self.assertEqual(ret['total'], 0)

    def test_get_all(self):

        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste1',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})
            planet_1 = ins_1.inserted_id
            ins_2 = planet.insert_one({'nome': 'teste planeta espécial',
                                       'terreno': 'liso',
                                       'clima': 'quente', 'filmes': 0})
            planet_2 = ins_2.inserted_id

        # este teste simula que o planeta de nome teste1 tem 8 filmes na swapi
        with patch.dict(self.planet_cache, {'teste1': 8}, clear=True):
            ret = self.app.get('/planet')
        ret = json.loads(ret.data)
        exp_ret = [
                {'_id': str(planet_1),
                 'clima': 'frio',
                 'filmes': 8,
                 'nome': 'teste1',
                 'terreno': 'acidentado'},
                {'_id': str(planet_2),
                 'clima': 'quente',
                 'filmes': 0,
                 'nome': 'teste planeta espécial',
                 'terreno': 'liso'}
        ]
        self.assertEqual(ret['result'], exp_ret)
        self.assertEqual(ret['total'], 2)

    def test_get_one_by_id_ok(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste1',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})
            planet_1 = ins_1.inserted_id

        ret = self.app.get('/planet/{}'.format(str(planet_1)))
        ret = json.loads(ret.data)
        exp_ret = {'_id': str(planet_1),
                   'clima': 'frio',
                   'filmes': 0,
                   'nome': 'teste1',
                   'terreno': 'acidentado'}
        self.assertEqual(ret['result'], exp_ret)

    def test_get_one_by_id_not_found(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste1',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})

        ret = self.app.get('/planet/5acbf0ed8a8b3800013017ff')
        self.assertEqual(ret.status_code, 404)

    def test_get_one_by_id_invalid(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste1',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})

        ret = self.app.get('/planet/blah')
        self.assertEqual(ret.status_code, 400)
        self.assertEqual(
                ret.data, '_id passado [blah] inválido'.encode('utf-8'))

    def test_get_one_by_name(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste planetá',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})
            planet_1 = ins_1.inserted_id

        ret = self.app.get('/planet/name/teste planetá')
        ret = json.loads(ret.data)
        exp_ret = {'_id': str(planet_1),
                   'clima': 'frio',
                   'filmes': 0,
                   'nome': 'teste planetá',
                   'terreno': 'acidentado'}
        self.assertEqual(ret['result'], exp_ret)

    def test_get_one_by_name_not_found(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste_planeta',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})
            planet_1 = ins_1.inserted_id

        ret = self.app.get('/planet/name/teste_planeta 2')
        self.assertEqual(ret.status_code, 404)

    def test_post_planet(self):
        data = {
            'clima': 'temperado',
            'nome': 'novo planeta',
            'terreno': 'árido'
        }
        ret = self.app.post('/planet', data=json.dumps(data),
                            content_type='application/json')
        self.assertEqual(ret.status_code, 200)
        ret = json.loads(ret.data)
        self.assertEqual(ret['result']['nome'], 'novo planeta')
        self.assertEqual(ret['result']['terreno'], 'árido')
        self.assertEqual(ret['result']['clima'], 'temperado')
        self.assertTrue('_id' in ret['result'])

    def test_post_planet_already_exists(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste_planeta',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})
            planet_1 = ins_1.inserted_id
        data = {
            'clima': 'temperado',
            'nome': 'teste_planeta',
            'terreno': 'árido'
        }
        ret = self.app.post('/planet', data=json.dumps(data),
                            content_type='application/json')
        self.assertEqual(ret.status_code, 400)
        self.assertEqual(
                ret.data,
                'O Planeta [teste_planeta] já existe'.encode('utf-8'))

    def test_delete_planet(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste_planeta',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})
            planet_1 = ins_1.inserted_id
        ret = self.app.delete('/planet/{}'.format(planet_1))
        self.assertEqual(ret.status_code, 204)

    def test_delete_planet_error(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste_planeta',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})
            planet_1 = ins_1.inserted_id
        ret = self.app.delete('/planet/1234')
        self.assertEqual(ret.status_code, 400)
        e_msg = "Erro deletando o planeta solicitado [1234] - '1234' is"\
                " not a valid ObjectId, it must be a 12-byte input or a"\
                " 24-character hex string".encode('utf-8')
        self.assertEqual(ret.data, e_msg)

    def test_edit_planet(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste_planeta',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})
            planet_1 = ins_1.inserted_id
        data = {'nome': 'teste_planeta',
                'terreno': 'acidentado',
                'clima': 'úmido'}
        ret = self.app.put('/planet/{}'.format(planet_1),
                           data=json.dumps(data),
                           content_type='application/json')
        self.assertEqual(ret.status_code, 200)
        ret = json.loads(ret.data)
        self.assertEqual(ret['result']['clima'], 'úmido')

    def test_edit_planet_invalid_id(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste_planeta',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})
            planet_1 = ins_1.inserted_id
        data = {'nome': 'teste_planeta',
                'terreno': 'acidentado',
                'clima': 'úmido'}
        ret = self.app.put('/planet/blah',
                           data=json.dumps(data),
                           content_type='application/json')
        self.assertEqual(ret.status_code, 400)
        self.assertEqual(
                ret.data, '_id passado [blah] inválido'.encode('utf-8'))

    def test_edit_planet_error(self):
        with self.ac.app_context():
            planet = self.mongo.db.planets
            ins_1 = planet.insert_one({'nome': 'teste_planeta',
                                       'terreno': 'acidentado',
                                       'clima': 'frio', 'filmes': 0})
            planet_1 = ins_1.inserted_id
        data = {'nome': 'teste_planeta',
                'terreno': 'acidentado',
                'clima': 'úmido'}
        ret = self.app.put('/planet/5acc154f14dac2000cea6eaa',
                           data=json.dumps(data),
                           content_type='application/json')
        self.assertEqual(ret.status_code, 400)
        exp_msg = 'Erro editando o planeta solicitado '\
                  '[5acc154f14dac2000cea6eaa] - _id não encontrado'
        self.assertEqual(ret.data, exp_msg.encode('utf-8'))

    def tearDown(self):
        self._clear_data()


if __name__ == '__main__':
    unittest.main()
