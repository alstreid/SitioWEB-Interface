from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
from usersModel import mongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/rgtmongodb'
mongo = PyMongo(app)

class Authenticated():
    
    @classmethod
    def login_auth(cls, username, password):
        try: 
            authenticated_user = None
            authenticated_user = mongo.db.admin.find_one({'username': username, 'password': password})
            # print (authenticated_user)
            if authenticated_user:
                return ({
                'username': authenticated_user['username'],
                'password': authenticated_user['password']
                })
                # return authenticated_user
            else:
                return {'message': 'Authentication login auth'}
        except: 
            return jsonify ({'message': "Error de autentificación"})
    
