from src.extensions import db

links = db.Table('user_email_link',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('email_id', db.Integer, db.ForeignKey('emailleads.id'), primary_key=True)
)