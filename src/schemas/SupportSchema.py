from . import ma
from src.models.SupportModel import SupportModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class SupportSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = SupportModel