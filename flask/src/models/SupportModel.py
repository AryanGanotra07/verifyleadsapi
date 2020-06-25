from src.extensions import db
import datetime
from typing import Dict, List, Union

class SupportModel(db.Model):
    __tablename__ = "support"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    status = db.Column(db.String(10))

    def __init__(self, name, email, message):
        self.name = name
        self.message = message
        self.email = email
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.status = "active"

    @classmethod
    def get_all(cls) -> List["SupportModel"]:
        return SupportModel.query.all()
    
    @classmethod
    def get_all_active(cls) -> List["SupportModel"]:
        return SupportModel.query.filter_by(status = "active").all()

    @classmethod
    def get_all_inactive(cls) -> List["SupportModel"]:
        return SupportModel.query.filter_by(status = "inactive").all()
    
    @classmethod
    def get_all_hold(cls) -> List["SupportModel"]:
        return SupportModel.query.filter_by(status = "hold").all()

    def save_to_db(self) -> None :
        db.session.add(self)
        db.session.commit()


