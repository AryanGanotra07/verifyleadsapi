from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required
from src.models.EmailModel import EmailModel
from src.models.UserModel import UserModel
import datetime
from src.verifier.EmailVerifier import EmailVerifier
from src.schemas.EmailSchema import EmailSchema
from flask_cors import cross_origin
#make constants for errors
email_schema = EmailSchema()
email_all_schema = EmailSchema(many=True)
def save_email_to_db(response):
    if response['code'] != 0:
        email = EmailModel(response['code'], response ['username'],response['domain'], response['email'], response['message'])
        email_from_db = EmailModel.find_email_by_address(email.email)
        if ('f_name' in response):
            print("f_name not null")
            email.f_name = response['f_name']
        if ('l_name' in response):
            email.l_name = response['l_name']
        if ('m_name' in response):
            email.m_name = response['m_name']
        print("Saving to db")
        #user = UserModel.find_by_id(user_id)
        if email_from_db is None:
            #email.users.append(user)
            email.save_to_db()
        else:
            email_from_db.code = email.code
            email_from_db.message = email.message
            email_from_db.modified_at = datetime.datetime.utcnow()
            if (email.f_name):
                print("f_name not null")
                email_from_db.f_name = email.f_name
            if (email.l_name):
                email_from_db.l_name = email.l_name
            if(email.m_name):
                email_from_db.m_name = email.m_name
            # email_from_db.owner_id = user_id
            email_from_db.save_to_db()
class Email(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('code',
    #         type = int,
    #         required = True,
    #         help = "This field cannot be left blank")
    # parser.add_argument('domain',
    #         type = str,
    #         required = True,
    #         help = "This field cannot be left blank")
    # parser.add_argument('email',
    #         type = str,
    #         required = True,
    #         help = "This field cannot be left blank")
    
    @classmethod
    #make all these class methods if they are not using self reference
    # @cross_origin(['https://verifyleads.io'])
    def get(cls, emailAddress : str):
        # print("Called b")
        # claims = get_jwt_claims()
        # print(claims)
        # if not claims['isAdmin']:
        #      return {'message' : 'Admin priviledge required'} , 401
        # user_id = get_jwt_identity()
        # print("Called")
        
        # # if email:
        #     return email.json()
        response = EmailVerifier.verify(emailAddress)
        email = EmailModel(response['code'], response ['username'],response['domain'], response['email'], response['message'])
        
        save_email_to_db(response)
        return (email_schema.dump(email))
    
   

#    # @jwt_required()
#     @fresh_jwt_required
#     def post(self, name : str):
#         if ItemModel.find_by_name(name) is not None:
#             return {'message' : "An item with name '{}' already exists".format(name)}, 400
#         data = Item.parser.parse_args()
#         item = ItemModel(name , **data)
#         try: 
#             item.save_to_db()
#         except:
#             return {'message' : 'An error has occurred while inserting item in the list'} , 500
#         return item.json(), 201

    # @jwt_required
    # def delete(self, name : str):
    #     claims = get_jwt_claims()
    #     if not claims['isAdmin']:
    #         return {'message' : 'Admin priviledge required'} , 401
    #     item = ItemModel.find_by_name(name)
    #     if item:
    #         item.delete_from_db()
    #     return ({'message' : 'Item deleted'})

    # def put(self, name : str):
       
    #     data = Item.parser.parse_args()
    #     item = ItemModel.find_by_name(name)
    #     if item is None:
    #         item = ItemModel(name,  **data)
    #     else:
    #         item.price = data['price']
    #         item.store_id = data['store_id']
    #     item.save_to_db()
    #     return item.json()
    



class EmailList(Resource) :
    #@jwt_required()
    @classmethod
    @jwt_required
    def get(cls):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
            return {'message' : 'Admin priviledge required'} , 401
        query = request.args.get('query')
        all_emails = EmailModel.find_all_emails()
        return email_all_schema.dump(all_emails), 201
        


class EmailFinder(Resource):
    @classmethod
    
    def get(cls):
        first_name = request.args.get('fname')
        last_name = request.args.get('lname')
        domain = request.args.get('domain')
        print(first_name, last_name, domain)

        print("Called b2")
        # claims = get_jwt_claims()
        # print(claims)
        # if not claims['isAdmin']:
        #      return {'message' : 'Admin priviledge required'} , 401
        # user_id = get_jwt_identity()
        # print("Called")
        
        # if email:
        #     return email.json()
        if (first_name is None or last_name is None or domain is None):
            return {"message" : "Field's can't be empty"}
        response = EmailVerifier.emailFinder(first_name.lower(), last_name.lower(), domain.lower())
        if (response['code'] == -1):
            return response
        # try:
        #     if (response['code'] != 1 or response['code'] != 2):
        #         return response
        # except:
        #     return {'code' : 0, 'message' : "Sorry, unable to lookup any emails."}
        email = EmailModel(response['code'], response ['username'],response['domain'], response['email'], response['message'])
        email.f_name = first_name
        email.l_name = last_name
        save_email_to_db(response)
        return (email_schema.dump(email)) , 201

class EmailFromDb(Resource):
    @classmethod
    @jwt_required
    def get(cls, email_id):
        claims = get_jwt_claims()
        print(claims)
        if not claims['isAdmin']:
             return {'message' : 'Admin priviledge required'} , 401
        return email_schema.dump(EmailModel.find_email_by_id(email_id))

        