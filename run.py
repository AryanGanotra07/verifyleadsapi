import os

"""
export FLASK_ENV=development
export DATABASE_URL=postgres://aryanganotra:Arnidara123#4@localhost:5432/email_verify_db
export JWT_SECRET_KEY=Arnidara123#4
export ADMIN_USERNAME=adminaryan9711
export ADMIN_PASSWORD=Arnidara123#
"""

from src.app import create_app as app
from src.app import create_socketio






if __name__ == '__main__':
   # add this line
   app = app()
   app.config['SECRET_KEY'] = 'secret!'
   socketio = create_socketio()

   
#   app.run(host='0.0.0.0')
   socketio.run(app, host='0.0.0.0')