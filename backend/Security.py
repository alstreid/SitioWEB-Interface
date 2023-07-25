from flask import Flask, request, jsonify, Response
import datetime
import jwt
import pytz
from decouple import config


class Security():
    secret=config('JWT_KEY')
    tz = pytz.timezone('America/Guayaquil')
    
    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            'iat': datetime.datetime.now( tz=cls.tz),
            'exp': datetime.datetime.now( tz=cls.tz)+datetime.timedelta(minutes=10),
            'username': authenticated_user['username']
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")
    
    @classmethod
    def validate_token(cls, encoded_token):
        try:
            payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
            print (payload)
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            return False