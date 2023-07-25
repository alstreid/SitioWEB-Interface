from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
from usersModel import Users
from Authenticated import Authenticated
from Security import Security
import jwt
from decouple import config


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/rgtmongodb'
mongo = PyMongo(app)
encoded_token = []
print (encoded_token)

#Ruta login

@app.route('/auth', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    # _user = (username,password)
    # print (_user)
    authenticated_user = Authenticated.login_auth(username, password)
    # print (authenticated_user)
    if (authenticated_user != None):
        global encoded_token 
        encoded_token = Security.generate_token(authenticated_user)
        # print (encoded_token)
        
        return encoded_token
          
    #     Identificado = True 
    #     response = {
    #         'estado': True,
    #         'token': encoded_token
    #     }
    # else:
    #     response = {
    #         'estado': False,
    #         'message': 'ERROR GEN'
    #     }

    # return jsonify(response)

#Rutas
@app.route('/login/<d_i>', methods=['GET'])
def login_client(d_i):
    login_client = Users.identify_client(d_i)
    
    return jsonify({'mensaje':'Documento de identidad válido',
                    'datos': login_client})

@app.route('/clients', methods=['POST'])
def create_client():
    if encoded_token:
        
        try:
            name = request.json['name']
            lastname = request.json['lastname']
            d_i = request.json['d_i']
            cel = request.json['cel']
            email = request.json['email']
            address = request.json['address']
  
            if name and lastname and d_i and cel and email and address:
                response = Users (name, lastname, d_i, cel, email, address)
                client_creado = response.crear_client()
                
                return jsonify({'mensaje':'Cliente Creado',
                            'data': client_creado})
            else: 
                return not_found()
        except: 
            return not_found()
    else: 
        return jsonify({'mensaje': 'No autorizado'})

@app.route('/clients', methods=['GET'])
def show_clients():
    if encoded_token:
        print(encoded_token)
        
        clients_list = Users.get_clients()

        return jsonify({'mensaje':'Lista de clientes',
                        'datos': clients_list})
    else:
        return jsonify({'mensaje': 'No autorizado'})

@app.route('/clients/<id>', methods=['GET'])
def show_client(id):

        client = Users.get_client(id)
        
        return jsonify({'mensaje':'Cliente por su ID',
                        'datos': client})


@app.route('/clients/<id>', methods=['DELETE'])
def drop_client(id):
    if encoded_token:
        del_client = Users.delete_client(id)
        
        return jsonify({'Cliente borrado': del_client})
    else: 
        return jsonify({'mensaje': 'No autorizado'})

@app.route('/clients/<id>', methods=['PUT'])
def update_client(id):
    if encoded_token:
        response = Users.put_client(id)
        return jsonify({'Cliente':response,
                        'Estado': 'ha sido actualizado'})
    else: 
        return jsonify({'mensaje': 'No autorizado'})
        
    
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify ({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)