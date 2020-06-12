from flask_restful import Resource, reqparse
from flask import request
from src.models.UserModel import UserModel
from src.blacklist import BLACKLIST
import datetime
from src.helpers.imageSaver import upload_to_aws
import json
from src.schemas.UserSchema import UserSchema
from flask_jwt_extended import get_raw_jwt, jwt_required, create_access_token, create_refresh_token,get_jwt_claims, jwt_refresh_token_required, get_jwt_identity

user_schema = UserSchema()
user_many_schema = UserSchema(many = True)
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
_user_parser.add_argument('password', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
_user_parser.add_argument('email', 
    type = str, 
    required = False,
    help = "This field can be blank for login")

_user_details_parser = reqparse.RequestParser()
_user_details_parser.add_argument('imgUrl', 
    type = str,
    required = False,
    
 )
_user_details_parser.add_argument('f_name', 
    type = str,
    required = False,
   
 )
_user_details_parser.add_argument('l_name', 
    type = str,
    required = False,
    
 )
_user_details_parser.add_argument('company', 
    type = str,
    required = False,
   
 )
 
 
 


class UserRegister(Resource):
    
    @classmethod
    @jwt_required
    def post(cls):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
             return {'message' : 'Admin priviledge required'} , 401
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user is not None:
            return {'message' : 'User with such username already exists'} , 400
        user = UserModel(**data)
        # user = user_schema.load(data)
        print(user)
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
        return user_schema.dump(user), 201
    
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

    @classmethod
    @jwt_required
    def post(cls, user_id : int):
        print("got request",user_id)
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {'message' : 'User do not exist'}, 404
        data = _user_details_parser.parse_args()
        imgUrl = data['imgUrl']
        imgData = (imgUrl.split(','))[1]
        print(imgData)
        # print("uploading to aws");
        resp = upload_to_aws(imgData, str(user.id)) 
        if (resp['code'] == 1):
            user.imgUrl = resp['imgUrl']
            user.update()
            return resp, 201
        return resp, 400
    
    @classmethod
    @jwt_required
    def put(cls, user_id : int):
        user = UserModel.find_by_id(user_id)
        if user is None:
            return {'message' : 'User do not exist'}, 404
        data = _user_details_parser.parse_args()
       
        try:
            user.updateFields(data['company'], data['f_name'], data['l_name'])
            return {'message' : 'User fields updated successfully'} , 201
        except:
            return {'message' : 'Error occurred while updating user field'} , 400


        

        
        


class UserLogin(Resource):
    

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
       
        if user and user.check_hash(data['password']):
            print(1)
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=user.id, fresh = True,expires_delta=expires)
            print(2)
            refresh_token = create_refresh_token(user.id)
            print(3)
            recents = UserModel.get_recent_accounts()
            return {
                'access_token' : access_token,
                'refresh_token' : refresh_token,
                'id' : user.id,
               

            }, 201
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

class UserList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
             return {'message' : 'Admin priviledge required'} , 401
        return user_many_schema.dump(UserModel.get_all_users())
            




