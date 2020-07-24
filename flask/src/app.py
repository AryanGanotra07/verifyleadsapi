
#src/app.py

from flask import Flask, jsonify, render_template,send_from_directory, request

from src.config import app_config
# from src.models import db, bcrypt # add this new line
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from src.blacklist import BLACKLIST
# from src.schemas import ma
from src.resources.User import UserLogin, RefreshToken, UserRegister, UserLogout, User, UserList
from src.resources.Email import Email, EmailFinder, EmailList, EmailFromDb
from src.shared.Authentication import identity, authenticate
from src.resources.Support import Support, SupportList
from src.extensions import db, bcrypt, ma, socketio, limiter
from flask_socketio import SocketIO,send
from src.resources.Graph import Graph
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

import os

#

def create_app():



  APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
  dotenv_path = os.path.join(APP_ROOT, '.env')
  load_dotenv(dotenv_path)

  env_name = os.environ.get('FLASK_ENV')

  print(os.path.join(os.getcwd(),'src','static'))
  app = Flask(__name__,static_url_path='/static')

  app.config.from_object(app_config[env_name])

  app.config.update(
      CELERY_BROKER_URL='redis://localhost:6379',
      CELERY_RESULT_BACKEND='redis://localhost:6379'
  )

#   limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["100 per day", "50 per hour"]
# )



  cors = CORS(app, resources={r"/*": {"origins": "https://verifyleads.io"}})

  # initializing bcrypt
  # bcrypt.init_app(app) # add this line

  # db.init_app(app) # add this line
  # ma.init_app(app)

  # from src.resources import celery
  

  extensions(app)

    
  
  
  api = Api(app)
  jwt = JWTManager(app)
  @app.after_request
  def after_request(response):
      white_origin= ['https://verifyleads.io','http://localhost:3000', 'https://app.verifyleads.io']
      if request.headers['Origin'] in white_origin:
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin'] 
        response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
      return response

  

  #   @jwt.invalid_token_loader

  #   @jwt.needs_refresh_token_loader

  #   @jwt.revoked_token_loader

  #   @jwt.unautorized_loader
  @jwt.user_claims_loader
  def add_claims_to_jwt(identity):
    from .models.UserModel import UserModel
    user = UserModel.find_by_id(identity)
    if user.isAdmin:
        print("returned is admin as true")
        return {'isAdmin' : True}
    print("returned is admin as false")
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


  


  api.add_resource(UserRegister, '/register')
  api.add_resource(User, '/user/<int:user_id>')
  api.add_resource(UserLogin, '/login')
  api.add_resource(RefreshToken, '/refresh')
  api.add_resource(UserLogout , '/logout')
  
  api.add_resource(Email,'/email/<string:emailAddress>')
  api.add_resource(EmailFinder,'/email')
  api.add_resource(Support, '/support')
  api.add_resource(SupportList, '/support/<string:query>')
  api.add_resource(EmailList, '/admin/emails/all')
  api.add_resource(Graph, '/admin/graph/all')
  api.add_resource(UserList, '/admin/users/all')
  api.add_resource(EmailFromDb, '/admin/email/<int:email_id>')

  #####################
  # existing code remain #
  ######################
 
  @app.route('/static/<path:path>')
  def send_js(path):
    return send_from_directory('static', path)
  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    print("Called");
    return render_template("home.html", content = "https://verifyleads.io")
  return app

 


def extensions(app):
  bcrypt.init_app(app) # add this line

  db.init_app(app) # add this line
  ma.init_app(app)
  limiter.init_app(app)
  
  @app.before_first_request
  def create_tables():
    db.create_all()
    from .models.UserModel import UserModel
    UserModel.create_admin()

def make_celery():
 
  from celery import Celery
  app = create_app()
  celery = Celery(
          app.import_name,
          backend=app.config['CELERY_RESULT_BACKEND'],
          broker=app.config['CELERY_BROKER_URL']
      )
  celery.conf.update(app.config)

  class ContextTask(celery.Task):
      def __call__(self, *args, **kwargs):
        with app.app_context():
          return self.run(*args, **kwargs)

  celery.Task = ContextTask
  return celery



# def create_socketio(app):
#   # app = create_app()
#   socketio = SocketIO(app = app,  cors_allowed_origins="*")
#   return socketio

  # @socketio.on("connect")
  # def onConnect():
  #   print("Connected")

  # @socketio.on("message")
  # def handleMessage(msg):
  #   print(msg)
  #   send(msg, broadcast=False)
    
  #   print("Csll")
    
  #   return None


app = create_app()
# socketio = create_socketio(app)
# import src.resources.socket