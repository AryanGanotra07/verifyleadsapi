from src.app import make_celery
from src.helpers.supportemail import sendEmail
from src.models.SupportModel import SupportModel
from src.models.EmailModel import EmailModel
from src.models.UserModel import UserModel
import datetime
from src.verifier.EmailVerifier import EmailVerifier
from flask_socketio import send, emit

celery = make_celery()

@celery.task(name='tasks.async_send_email')
def async_send_email(data):
    print("called")
    support = SupportModel(**data)
    support.save_to_db()
    sendEmail(data)
    print("Executed")

@celery.task(name='tasks.save_email_to_db')
def save_email_to_db(response):
    if response['code'] != 0:
        email = EmailModel(response['code'], response ['username'],response['domain'], response['email'], response['message'])
        email_from_db = EmailModel.find_email_by_address(email.email)
        if ('f_name' in response):
            print("f_name not null")
            email.f_name = response['f_name']
        if ('l_name' in response):
            email.l_name = response['l_name']
        if ('m_name' in response):
            email.m_name = response['m_name']
        print("Saving to db")
        #user = UserModel.find_by_id(user_id)
        if email_from_db is not None:
            #email.users.append(user)
            email.save_to_db()
        else:
            email_from_db.code = email.code
            email_from_db.message = email.message
            email_from_db.modified_at = datetime.datetime.utcnow()
            if (email.f_name):
                print("f_name not null")
                email_from_db.f_name = email.f_name
            if (email.l_name):
                email_from_db.l_name = email.l_name
            if(email.m_name):
                email_from_db.m_name = email.m_name
            # email_from_db.owner_id = user_id
            email_from_db.save_to_db()


@celery.task(name = "tasks.async_verify_email")
def verifyEmail(email):
    print("Executing for email - ", email)
    response= EmailVerifier.verify(email)
    # if(response['code'] == 1):
    #     print(response['email'])
    # return response
    # if (response['code'] == 1):
    emit("email-finder-result",  "Got it")
    
    return None
