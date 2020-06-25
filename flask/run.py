import os
from src.app import app
# from src.app import socketio
# from src.app import create_socketio






if __name__ == '__main__':
   # add this line
   
   app.config['SECRET_KEY'] = 'secret!'
   
   

   
   app.run(host='0.0.0.0')
   # socketio.run(app, host='0.0.0.0')