from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import Flask
from flask import request
from flask import jsonify


app = Flask('swplanetapi')
app.config['MONGO_DBNAME'] = 'swapidb'
# rodando no docker-compose up meu mongodb service se chama mongodb :)
app.config['MONGO_URI'] = 'mongodb://mongodb:27017/{}'.format(
    app.config['MONGO_DBNAME'])


@app.route('/planet', methods=['GET'])
def get_all_planets():
    planet = mongo.db.planets
    output = []
    for p in planet.find():
        output.append({'_id': str(p['_id']), 'nome': p['nome'],
                       'clima': p['clima'], 'terreno': p['terreno'],
                       'filmes': p['filmes']})
    return jsonify({'result': output, 'total': len(output)})


@app.route('/planet/<planet_id>', methods=['GET'])
def get_one_planet_by_id(planet_id):
    planet = mongo.db.planets
    try:
        p = planet.find_one_or_404({'_id': ObjectId(planet_id)})
    except InvalidId as e:
        code = 400
        msg = '_id passado [{}] inválido'.format(planet_id)
        return (msg, code)

    output = {}
    if p:
        output = {'_id': str(p['_id']), 'nome': p['nome'],
                  'clima': p['clima'], 'terreno': p['terreno'],
                  'filmes': p['filmes']}
        return jsonify({'result': output})


@app.route('/planet/name/<planet_name>', methods=['GET'])
def get_one_planet_by_name(planet_name):
    planet = mongo.db.planets
    p = planet.find_one_or_404({'nome': planet_name})
    output = {}
    if p:
        output = {'_id': str(p['_id']), 'nome': p['nome'],
                  'clima': p['clima'], 'terreno': p['terreno'],
                  'filmes': p['filmes']}
    return jsonify({'result': output})


@app.route('/planet', methods=['POST'])
def add_star():
    planet = mongo.db.planets
    planet_data = {
        "nome": request.json['nome'],
        "clima": request.json['clima'],
        "terreno": request.json['terreno'],
        "filmes": 0
    }
    p = planet.find_one({'nome': planet_data['nome']})
    if p:
        code = 400
        msg = 'O Planeta [{}] já existe'.format(planet_data['nome'])
        return (msg, code)
    else:
        ins = planet.insert_one(planet_data)
        planet_id = ins.inserted_id
        new_planet = planet.find_one({'_id': planet_id})
        output = {}
        for item in planet_data:
            output[item] = new_planet[item]
        output['_id'] = str(new_planet['_id'])

    return jsonify({'result': output})


@app.route('/planet/<planet_id>', methods=['DELETE'])
def delete_one_planet_by_id(planet_id):
    planet = mongo.db.planets
    try:
        ret = planet.delete_one({'_id': ObjectId(planet_id)})
        if ret.deleted_count < 1:
            raise Exception('_id não encontrado')
        msg = ''
        code = 204
    except Exception as e:
        msg = 'Erro deletando o planeta solicitado [{}] - {}'.format(
            planet_id, e)
        code = 400
    return (msg, code)


if __name__ == '__main__':
    mongo = PyMongo(app)
    app.run(host="0.0.0.0", debug=True)
