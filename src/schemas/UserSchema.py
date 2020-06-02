from src.extensions import ma
from src.models.UserModel import UserModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field,fields
from src.schemas.EmailSchema import EmailSchema
class UserSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = UserModel
  password = auto_field(load_only = True)
  # emailleads = fields.Nested(EmailSchema, many = True)
  """
  User Schema
  """
  # id = fields.Int(dump_only=True)
  # name = fields.Str(required=True)
  # email = fields.Email(required=True)
  # password = fields.Str(required=True)
  # created_at = fields.DateTime(dump_only=True)
  # modified_at = fields.DateTime(dump_only=True)
  # blogposts = fields.Nested(EmailSchema, many=True)