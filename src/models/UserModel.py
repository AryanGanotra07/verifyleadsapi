import datetime
import os
from src.extensions import db
from src.extensions import bcrypt
from marshmallow import fields, Schema
from .EmailModel import EmailSchema
from typing import Dict, List, Union
from src.models.EmailModel import EmailJSON
from src.helpers.dbhelper import links
UserJSON = Dict[str, Union[List[EmailJSON],str, int]]




class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    f_name = db.Column(db.String(128), nullable = True)
    l_name = db.Column(db.String(128), nullable = True)
    #email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now().date())
    modified_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    imgUrl = db.Column(db.String(128), default = None, nullable = True)
    company = db.Column(db.String(128), default = None, nullable = True)
    email = db.Column(db.String(128), default = "sample")
    emailleads = db.relationship('EmailModel',secondary = links ,backref = db.backref('users', lazy=True))
    isAdmin = db.Column(db.Boolean, nullable = False, default = False)

    def __init__(self, username, password,isAdmin = False):
        """
        Class constructor
        """
        self.username = username
        #self.email = email
        self.password = self.__generate_hash(password)
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.isAdmin = isAdmin
        
           

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def update(self) -> None:
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users() -> List["UserModel"]:
        return UserModel.query.all()
    
    @staticmethod
    def get_recent_accounts() -> List["UserModel"]:
        current_date = datetime.datetime.utcnow()
        from_date = current_date - datetime.timedelta(days = 7)
        recents = UserModel.query.with_entities(UserModel.created_at).filter(UserModel.created_at >= from_date).all()
        return recents


    @staticmethod
    def create_admin()->None:
        adminUsername = os.environ.get("ADMIN_USERNAME")
        adminPassword = os.environ.get("ADMIN_PASSWORD")
        if not UserModel.find_by_username(adminUsername):
            user = UserModel(adminUsername, adminPassword, True)
            user.save_to_db()

    @classmethod
    def find_by_username(cls, username : str) -> "UserModel":
        user = cls.query.filter_by(username = username).first()
        return user

    @classmethod
    def find_by_id(cls, _id : int) -> "UserModel":
        user = cls.query.filter_by(id = _id).first()
        return user

  
    def json(self) -> UserJSON:
        return {'id' : self.id, 'username' : self.username}

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  # add this new method
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)



class UserSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  username = fields.Str(required=True)
  #email = fields.Email(required=True)
  password = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  emailleads = fields.Nested(EmailSchema, many=True)
  isAdmin = fields.Boolean(required = True)