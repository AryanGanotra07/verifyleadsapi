import datetime
import os
from src.extensions import db
from src.extensions import bcrypt
from marshmallow import fields, Schema
from .EmailModel import EmailSchema
from typing import Dict, List, Union
from src.models.EmailModel import EmailJSON
from src.helpers.dbhelper import links
from sqlalchemy import desc
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

    def __init__(self, username,email, password,isAdmin = False):
        """
        Class constructor
        """
        self.username = username
        self.email = email
        self.password = self.__generate_hash(password)
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.isAdmin = isAdmin
        
           

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def update(self) -> None:
        db.session.commit()
    
    def updateFields(self,company,f_name,l_name) -> None:
        print(company, f_name, l_name);
        if(f_name):
            self.f_name = f_name
        if(l_name):
            self.l_name = l_name
        if(company):
            self.company = company
        self.update()
       


    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users() -> List["UserModel"]:
        return UserModel.query.with_entities(UserModel.id, UserModel.username, UserModel.email,UserModel.company, UserModel.created_at).order_by(desc(UserModel.created_at)).all()
    
    @staticmethod
    def get_recent_accounts() -> List["UserModel"]:
        current_date = datetime.datetime.utcnow()
        from_date = current_date - datetime.timedelta(days = 50)
        sql  = "SELECT date(created_at), count(created_at) as total_count FROM users WHERE created_at >= '{from_date}' GROUP BY date(created_at) ORDER BY date(created_at) ASC".format(from_date = from_date)
        recents = db.engine.execute(sql)
        sqlCount = "SELECT count(id) FROM users"
        total = db.engine.execute(sqlCount).fetchone()
        total = total[0]
        dates = []
        counts = []
        for recent in recents.fetchall():
            # result.append({
            #     'date' : str(recent[0]),
            #     'count' : recent[1]
            # });
            dates.append(str(recent[0]))
            counts.append(recent[1])
        result = {
            'labels' : dates,
            'counts' : counts,
            'total' : total
        }
        return result


    @staticmethod
    def create_admin()->None:
        adminUsername = os.environ.get("ADMIN_USERNAME")
        adminPassword = os.environ.get("ADMIN_PASSWORD")
        adminEmail = os.environ.get("ADMIN_EMAIL")
        if not UserModel.find_by_username(adminUsername):
            user = UserModel(adminUsername,adminEmail, adminPassword, True)
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