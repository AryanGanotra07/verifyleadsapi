from src.extensions import db
import datetime
from marshmallow import fields, Schema
from typing import Dict, List, Union

EmailJSON = Dict[str, Union[int, str]]

class EmailModel(db.Model):
    __tablename__ = "emailleads"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    domain = db.Column(db.String(128))
    email = db.Column(db.String(128),unique=True, nullable=False)
    message = db.Column(db.String(200), nullable = False)
    username = db.Column(db.String(200), nullable = False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
   # owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, code,username, domain, email, message):
        
        self.code = code
        self.domain = domain
        self.username = username
        self.email = email
        self.message = message
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
      #  self.owner_id = owner_id
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def find_all_emails() -> List["EmailModel"]:
        return EmailModel.query.all()
  
    @staticmethod
    def find_email_by_id(id : int) -> "EmailModel":
        return EmailModel.query.get(id)

    @staticmethod
    def find_email_by_address(email : str) -> "EmailModel":
        print("finding email by address")
        email = EmailModel.query.filter_by(email = email).first()
        return email

    @staticmethod
    def find_email_by_email_and_user(emailId : int, userId : int ) -> "EmailModel":
        email = EmailModel.query.filter_by(id = emailId).filter(EmailModel.users.any(id = userId)).first()
        return email

    def json(self) -> EmailJSON:
        return {'id' : self.id,
         'email' : self.email, 
         'code' : self.code, 
         'username' : self.username,
         'domain' : self.domain,
          'message' : self.message, 
          "user_id" : self.owner_id}
    
class EmailSchema(Schema):
  """
  Email Schema
  """
  id = fields.Int(dump_only=True)
  code = fields.Int(required=True)
  email = fields.Str(required=True)
  domain = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  #owner_id = fields.Int(required=True)
  message = fields.Str(required = True)