from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO, send
socketio = SocketIO()
limiter = Limiter(key_func=get_remote_address, default_limits=["100 per day", "100 per hour"])

ma = Marshmallow()


db = SQLAlchemy()
bcrypt = Bcrypt()