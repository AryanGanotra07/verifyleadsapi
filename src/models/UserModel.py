import datetime
from . import db
from ..app import bcrypt
from marshmallow import fields, Schema
from .EmailModel import EmailSchema


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    #email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    emailleads = db.relationship('EmailModel', backref='users', lazy=True)

    def __init__(self, username, password):
        """
        Class constructor
        """
        self.username = username
        #self.email = email
        self.password = self.__generate_hash(password)
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

  
    def __repr(self):
        return '<id {}>'.format(self.id)

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