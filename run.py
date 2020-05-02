import os
"""
export FLASK_ENV=development
export DATABASE_URL=postgres://aryanganotra:Arnidara123#4@localhost:5432/email_verify_db
export JWT_SECRET_KEY=Arnidara123#4
export ADMIN_USERNAME=adminaryan9711
export ADMIN_PASSWORD=Arnidara123#
"""

from src.app import app as app

if __name__ == '__main__':

  app.run(host='0.0.0.0')
