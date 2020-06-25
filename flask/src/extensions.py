from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

from flask_socketio import SocketIO, send
socketio = SocketIO()


ma = Marshmallow()


db = SQLAlchemy()
bcrypt = Bcrypt()