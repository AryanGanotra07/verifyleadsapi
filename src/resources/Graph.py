from flask_restful import Resource
from src.models.UserModel import UserModel
from flask_jwt_extended import get_jwt_claims, jwt_required

class Graph(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
             return {'message' : 'Admin priviledge required'} , 401
        return UserModel.get_recent_accounts()
