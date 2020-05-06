from . import ma
from src.models.EmailModel import EmailModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class EmailSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = EmailModel
    include_fk = False

  """
  id = fields.Int(dump_only=True)
  code = fields.Int(required=True)
  email = fields.Str(required=True)
  domain = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  owner_id = fields.Int(required=True) """