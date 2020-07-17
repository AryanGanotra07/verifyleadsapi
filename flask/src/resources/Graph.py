from flask_restful import Resource
from src.models.UserModel import UserModel
from flask import request
from flask_jwt_extended import get_jwt_claims, jwt_required

class Graph(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
             return {'message' : 'Admin priviledge required'} , 401
        print(request.remote_addr)
        return UserModel.get_recent_accounts()
