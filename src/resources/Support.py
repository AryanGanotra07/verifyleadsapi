from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from src.models.SupportModel import SupportModel
from src.schemas.SupportSchema import SupportSchema
import requests
from src.helpers.supportemail import sendEmail

support_schema = SupportSchema(many = True)
_support_parser = reqparse.RequestParser()
_support_parser.add_argument('name', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
_support_parser.add_argument('email', 
    type = str, 
    required = True,
    help = "This field cannot be blank")
_support_parser.add_argument('message', 
    type = str, 
    required = True,
    help = "This field cannot be blank")

class Support(Resource):
    @classmethod
    def post(cls):
        data = _support_parser.parse_args()
        support = SupportModel(**data)
        support.save_to_db()
        sendEmail(data)
        
        return {"message" : "We will get back to you shortly."} , 201
    
   
    @classmethod
    @jwt_required
    def get(cls):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
            return {'message' : 'Admin priviledge required'} , 401
        supports = SupportModel.get_all()
        return support_schema.dump(supports) , 201

class SupportList(Resource):
    @classmethod
    @jwt_required
    def get(cls, query):
        if(query == "active"):
            supports = SupportModel.get_all_active()
            return support_schema.dump(supports) , 201
        elif(query == "inactive"):
            supports = SupportModel.get_all_inactive()
            return support_schema.dump(supports) , 201
        elif(query == "hold"):
            supports = SupportModel.get_all_hold()
            return support_schema.dump(supports) , 201
        else:
            return {'message' : 'Unable to parse the query'} , 401







