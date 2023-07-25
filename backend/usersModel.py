from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util, ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/rgtmongodb'
mongo = PyMongo(app)

# sdadasdasdasdasdas
class Users:
   def __init__(self, name, lastname, d_i, cel, email, address): 
      # , t_c, p_p,c_afil
        self.name = name
        self.lastname = lastname
        self.d_i = d_i
        self.cel = cel
        self.email = email
        self.address = address
        

   def crear_client(self):
      id = mongo.db.clients.insert_one({'name':self.name,'lastname': self.lastname,'d_i':self.d_i,'cel':self.cel,'email':self.email, 'address':self.address}) 
      user_id = str(id.inserted_id) 
      
      response = {
         '_id': user_id,
         'name': self.name,
         'lastname': self.lastname,
         'd_i': self.d_i,
         'cel': self.cel,
         'email': self.email,
         'address': self.address

      }
      return response
   
      # import random
      # import string
      # def generar_contrasena(longitud):
      #    caracteres = string.ascii_letters + string.digits + string.punctuation
      #    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
      #    return contrasena

      # # Ejemplo: Generar una contraseña de longitud 12
      # contrasena_generada = generar_contrasena(12)
      # print("Contraseña generada:", contrasena_generada)

   # def edit_password():
      
   
   def get_clients():
      clients = []
      for doc in mongo.db.clients.find():
         clients.append({
           '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'lastname': doc['lastname'],
            'd_i': doc['d_i'],
            'cel': doc['cel'],
            'email': doc['email'],
            'address': doc['address']
            
        })
      return (clients)
 
   def get_client(id):
    client = mongo.db.clients.find_one({'_id': ObjectId(id)})
    return ({
        '_id': str(ObjectId(client['_id'])),
        'name': client['name'],
         'lastname': client['lastname'],
         'd_i': client['d_i'],
         'cel': client['cel'],
         'email': client['email'],
         'address': client['address']
    })
   
   def identify_client(d_i):
      # c_i = request.jsonc_i['c_i']
      client = mongo.db.clients.find_one({'d_i': d_i})
      cedula = d_i
      if client:
         return ({
         'name': client['name'],
         'lastname': client['lastname'],
         'id': cedula
         })
      else:
         return {'Estado':'Número de documento inválido'}
      
    
   def delete_client(id):
    mongo.db.clients.delete_one({'_id': ObjectId(id)})
    del_client = id
    return (del_client)
 
   def put_client(id):
      name = request.json['name']
      lastname = request.json['lastname']
      d_i = request.json['d_i']
      cel = request.json['cel']
      email = request.json['email']
      address = request.json['address']
    
      if name and lastname and d_i and cel and email and address:
         mongo.db.clients.update_one({'_id': ObjectId(id)}, {'$set': {
               'name': name, 
               'lastname': lastname, 
               'd_i':d_i,
               'cel': cel,
               'email': email,
               'address': address
         }})
         response = id
         return response
   
   