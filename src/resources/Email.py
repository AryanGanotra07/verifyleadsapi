from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required
from src.models.EmailModel import EmailModel
from src.models.UserModel import UserModel
import datetime
from src.verifier.EmailVerifier import EmailVerifier
from src.schemas.EmailSchema import EmailSchema
#make constants for errors
email_schema = EmailSchema()
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
    @jwt_required
    #make all these class methods if they are not using self reference
    def get(cls, emailAddress : str):
        print("Called b")
        claims = get_jwt_claims()
        print(claims)
        if not claims['isAdmin']:
             return {'message' : 'Admin priviledge required'} , 401
        user_id = get_jwt_identity()
        print("Called")
        
        # if email:
        #     return email.json()
        response = EmailVerifier.verify(emailAddress)
        email = EmailModel(response['code'], response ['username'],response['domain'], response['email'], response['message'])
        from src.resources.Tasks import save_email_to_db
        save_email_to_db.delay(response, user_id)
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
    



# class ItemList(Resource) :
#     #@jwt_required()
#     @jwt_optional
#     def get(self):
#         # connection = sqlite3.connect("data.db")
#         # cursor = connection.cursor()
#         # query = "SELECT * FROM items"
#         # result = cursor.execute(query)
#         # items = []
#         # for row in result:
#         #     items.append({
#         #         'name' : row[0],
#         #         'price' : row[1]
#         #     })
#         # connection.close()
#         user_id = get_jwt_identity()
#         if user_id:
#             return {'items' : [item.json for item in ItemModel.find_all()]} , 200
#         return {'items' : [item.json for item in ItemModel.find_all()]} , 200


class EmailFinder(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        first_name = request.args.get('fname')
        last_name = request.args.get('lname')
        domain = request.args.get('domain')
        print(first_name, last_name, domain)

        print("Called b2")
        claims = get_jwt_claims()
        print(claims)
        if not claims['isAdmin']:
             return {'message' : 'Admin priviledge required'} , 401
        user_id = get_jwt_identity()
        print("Called")
        
        # if email:
        #     return email.json()
        if (first_name is None or last_name is None or domain is None):
            return {"message" : "Field's can't be empty"}
        response = EmailVerifier.emailFinder(first_name, last_name, domain)
        email = EmailModel(response['code'], response ['username'],response['domain'], response['email'], response['message'])
        email.f_name = first_name
        email.l_name = last_name
        from src.resources.Tasks import save_email_to_db
        save_email_to_db.delay(response, user_id)
        return (email_schema.dump(email))
        