from src.app import make_celery
from src.helpers.supportemail import sendEmail
from src.models.SupportModel import SupportModel
from src.models.EmailModel import EmailModel
from src.models.UserModel import UserModel
import datetime
celery = make_celery()

@celery.task(name='tasks.async_send_email')
def async_send_email(data):
    print("called")
    support = SupportModel(**data)
    support.save_to_db()
    sendEmail(data)
    print("Executed")

@celery.task(name='tasks.async_save_to_db')
def save_email_to_db(response, user_id):
    if response['code'] != 0:
        email = EmailModel(response['code'], response ['username'],response['domain'], response['email'], response['message'])
        email_from_db = EmailModel.find_email_by_address(email.email)
        print("Saving to db")
        user = UserModel.find_by_id(user_id)
        if email_from_db not in user.emailleads:
            email.users.append(user)
            email.save_to_db()
        else:
            email_from_db.code = email.code
            email_from_db.message = email.message
            email_from_db.modified_at = datetime.datetime.utcnow()
            # email_from_db.owner_id = user_id
            email_from_db.save_to_db()
    pass