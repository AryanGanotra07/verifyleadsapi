
#src/app.py

from flask import Flask, jsonify

from .config import app_config
from .models import db, bcrypt # add this new line
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager
from src.blacklist import BLACKLIST
from src.resources.User import UserLogin, RefreshToken, UserRegister, UserLogout, User
from src.resources.Email import Email
from src.shared.Authentication import identity, authenticate


def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])


  # initializing bcrypt
  bcrypt.init_app(app) # add this line

  db.init_app(app) # add this line
  from .models import UserModel, EmailModel
  api = Api(app)
  jwt = JWTManager(app)

  @jwt.user_claims_loader
  def add_claims_to_jwt(identity):
    if identity == 1:
        return {'isAdmin' : True}
    return {'isAdmin' : False}

  @jwt.token_in_blacklist_loader
  def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

  @jwt.expired_token_loader
  def expired_token_callback():
    return jsonify({
        'description' : 'The token has expired..',
        'error' : 'token_expired'
    }) , 401

#   @jwt.invalid_token_loader

#   @jwt.needs_refresh_token_loader

#   @jwt.revoked_token_loader

#   @jwt.unautorized_loader



  

  api.add_resource(UserRegister, '/register')
  api.add_resource(User, '/user/<int:user_id>')
  api.add_resource(UserLogin, '/login')
  api.add_resource(RefreshToken, '/refresh')
  api.add_resource(UserLogout , '/logout')
  api.add_resource(Email,'/email/<string:emailAddress>')
  
  #####################
  # existing code remain #
  ######################
  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your first endpoint is workin'
  

  return app