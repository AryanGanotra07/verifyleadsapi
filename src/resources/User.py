from flask_restful import Resource, reqparse
from flask import request
from src.models.UserModel import UserModel
from src.blacklist import BLACKLIST
from flask_jwt_extended import get_raw_jwt, jwt_required, create_access_token, create_refresh_token,get_jwt_claims, jwt_refresh_token_required, get_jwt_identity

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
_user_parser.add_argument('password', 
    type = str, 
    required = True,
    help = "This field cannot be blank")


class UserRegister(Resource):
    
    @classmethod
    
    def post(cls):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
             return {'message' : 'Admin priviledge required'} , 401
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user is not None:
            return {'message' : 'User with such username already exists'} , 400
        user = UserModel(**data)
        user.save_to_db()

        return ({'message' : 'User created successfully.'}), 201

class User(Resource):

    @classmethod
    @jwt_required
    def get(cls, user_id : int):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
             print("This is admin")
             return {'message' : 'Admin priviledge required'} , 401
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message', 'user not found'} , 404
        return user.json();
    
    @classmethod
    @jwt_required
    def delete(cls, user_id : int):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
             return {'message' : 'Admin priviledge required'} , 401
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message' : 'User not found'} , 404
        user.delete_from_db()
        return {'message' : 'user deleted successfully'} , 200

class UserLogin(Resource):
    

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and user.check_hash(data['password']):
            print(1)
            access_token = create_access_token(identity=user.id, fresh = True)
            print(2)
            refresh_token = create_refresh_token(user.id)
            print(3)
            return {
                'access_token' : access_token,
                'refresh_token' : refresh_token
            }, 200
            print(4)
        return {'message' : 'Return invalid credentials'}, 401


class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity = get_jwt_identity, fresh = False)
        return {'access_token' : new_token} , 200

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message' : 'successfully logged out'}
