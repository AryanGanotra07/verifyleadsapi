from . import db
import datetime
from marshmallow import fields, Schema


class EmailModel(db.Model):
    __tablename__ = "emailleads"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    domain = db.Column(db.String(128))
    email = db.Column(db.String(128),unique=True, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, data):
        
        self.code = data.get('code')
        self.domain = data.get('domain')
        self.email = data.get('email')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.owner_id = data.get('owner_id')
    
    def save(self):
        db.session.save(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_all_emails():
        return EmailModel.query.all()
  
    @staticmethod
    def get_one_email(id):
        return EmailModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
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
  owner_id = fields.Int(required=True)