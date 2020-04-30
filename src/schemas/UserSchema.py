from . import fields, Schema
import EmailSchema
class UserSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  blogposts = fields.Nested(EmailSchema, many=True)