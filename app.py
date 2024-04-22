from flask import Flask, request
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@projagil.pim4mny.mongodb.net/APS5'
mongo = PyMongo(app)

########################################################################################################3
#Usuários
@app.route('/usuarios', methods = ['GET'])
def get_all_users():
    filtro = {}
    projecao = {'_id': 0}
    dados_usuarios = mongo.db.usuarios.find(filtro, projecao)
    resp = {
        'usuarios' : list(dados_usuarios)
    }
    return resp, 200
    
@app.route('/usuarios/<string:id_usuario>', methods=['GET'])
def user_get_id(id_usuario):
    filtro = {"_id": ObjectId(id_usuario)}

    user = mongo.db.usuarios.find_one(filtro)
    if user:
        return {'usuario': str(user)}
    else:
        return {'mensagem':'usuário não encontrado'}, 404

@app.route('/usuarios', methods = ['POST'])
def post_user():
    data = request.json

    if "cpf" not in data:
        return {'erro':'cpf é obrigatório'}
    
    result = mongo.db.usuarios.insert_one(data)

    return {"id": str(result.inserted_id)}, 201

@app.route('/usuarios/<string:id_usuario>', methods = ['PUT'])
def update_user(id_usuario):
    data = request.json

    filtro = {"_id": ObjectId(id_usuario)}

    user = mongo.db.usuarios.find_one(filtro)
    if not user:
        return {"erro": "usuário não encontrado"}, 404
    else:
        user = mongo.db.usuarios.update_one(filtro, {"$set":data})
        return {'mensagem':'Usuário atualizado com sucesso'}, 201

@app.route('/usuarios/<string:id_usuario>', methods=['DELETE'])
def delete_user(id_usuario):
    filtro = {"_id": ObjectId(id_usuario)}

    user = mongo.db.usuarios.find_one(filtro)
    if not user:
        return {"erro": "usuário não encontrado"}, 404
    else:
        user = mongo.db.usuarios.delete_one(filtro)
        return {'mensagem':'Usuário deletado com sucesso'}, 200

##########################################################################################
#Bikes
@app.route('/bikes', methods = ['GET'])
def get_all_bikes():
    filtro = {}
    projecao = {'_id': 0}
    dados_bikes = mongo.db.bikes.find(filtro, projecao)
    resp = {
        'bikes' : list(dados_bikes)
    }
    return resp, 200
    
@app.route('/bikes/<string:id_bike>', methods=['GET'])
def bike_get_id(id_bike):
    filtro = {"_id": ObjectId(id_bike)}
    bike = mongo.db.bikes.find_one(filtro)
    if bike:
        return {'bike': str(bike)}, 200
    else:
        return {"erro": "bike não encontrada"}, 404

@app.route('/bikes', methods = ['POST'])
def post_bike():
    data = request.json
    
    result = mongo.db.bikes.insert_one(data)

    return {"id": str(result.inserted_id)}, 201

@app.route('/bikes/<string:id_bike>', methods = ['PUT'])
def update_bike(id_bike):
    data = request.json

    filtro = {"_id": ObjectId(id_bike)}

    bike = mongo.db.bikes.find_one(filtro)
    if not bike:
        return {"erro": "bike não encontrada"}, 404
    else:
        bike = mongo.db.bikes.update_one(filtro, {"$set":data})
        return {'mensagem':'Bike atualizada com sucesso'}, 201

@app.route('/bikes/<string:id_bike>', methods=['DELETE'])
def delete_bike(id_bike):
    filtro = {"_id": ObjectId(id_bike)}

    bike = mongo.db.bikes.find_one(filtro)
    if not bike:
        return {"erro": "bike não encontrada"}, 404
    else:
        bike = mongo.db.bikes.delete_one(filtro)
        return {'mensagem':'Bike deletada com sucesso'}, 200

#############################################################################3
#Empréstimos
@app.route('/emprestimos', methods=['GET'])
def get_all_lendings():
    filtro = {}
    projecao = {'_id':0}
    emprestimos = mongo.db.emprestimos.find(filtro, projecao)
    resp = {
        'emprestimos' : list(emprestimos)
    }
    return resp, 200

@app.route('/emprestimos', methods = ['POST'])
def create_lending():
    data = request.json
    id_bike = data.get('id_bike')
    id_usuario = data.get('id_usuario')

    if not id_bike or not id_usuario:
        return {'erro':'id_bike e id_usuario são obrigatórios'}
    else:
        emprestimo = {
        'id_bike': id_bike,
        'id_usuario': id_usuario,
        'data_emprestimo': datetime.utcnow()
    }
    
    result = mongo.db.emprestimos.insert_one(emprestimo)
    return {'id': str(result.inserted_id)}, 201

@app.route('/emprestimos/<string:id_usuario>', methods=['GET'])
@app.route('/emprestimos/<string:id_bike>', methods=['GET'])
@app.route('/emprestimos/<string:id_usuario>/<string:id_bike>', methods=['GET'])
def get_landing_id(id_usuario=None, id_bike=None):
    id_bike = request.args.get('id_bike', id_bike)  # Prioritize path variable, fallback to query parameter if not available

    if not id_usuario and not id_bike:
        return {'erro': 'Pelo menos um ID (usuário ou bicicleta) deve ser fornecido'}, 400

    filtro = {}
    if id_usuario:
        filtro['id_usuario'] = id_usuario
    if id_bike:
        filtro['id_bike'] = id_bike

    emprestimo = mongo.db.emprestimos.find_one(filtro)
    if emprestimo:
        emprestimo['_id'] = str(emprestimo['_id'])
        if 'id_usuario' in emprestimo:
            emprestimo['id_usuario'] = str(emprestimo['id_usuario'])
        if 'id_bike' in emprestimo:
            emprestimo['id_bike'] = str(emprestimo['id_bike'])
        return {'empréstimo': emprestimo}, 200
    else:
        return {'erro': 'Empréstimo não encontrado'}, 404
   
if __name__ == '__main__':
    app.run(debug=True)
