import json
import smtplib
import dns.resolver
import dns.exception
import uuid
from src.verifier.regex_check import regex_check
import re
import socket
import random


EMAIL_INVALID_RESULT = {'code':0, 'message': "Email address format is invalid. Please enter a valid email address."}
class EmailVerifier:

    

    def __init__(self, email) :
        self.email = email
        
    
    def verify(self):
        
        result = {'code':0, 'message': "Unknown exception occurred. Please try again later."}
        regexVerified = regex_check(self.email)
        if (regexVerified != True):
            print("Invalid regex")
            return EMAIL_INVALID_RESULT
        username, domain = "", ""
        try:
            username_r, domain_r = self._get_domain_from_email_address(self.email)
            username = username_r[1]
            domain = domain_r[1]
            print(username, domain)
        except TypeError:
            return EMAIL_INVALID_RESULT
        except IndexError:
            return EMAIL_INVALID_RESULT
        mail_servers = []
        try:
            mail_servers = sorted([x for x in dns.resolver.query(domain, 'MX')], key=lambda k: k.preference)
        except dns.exception.Timeout as ex:
            result = {'code':5, 'message': 'DNS Lookup Timeout', }
        except dns.resolver.NXDOMAIN as ex:
            result = {'code':4, 'message': 'Mail server not found for domain'}
        except Exception as ex:
            result = {'code':0, 'message': 'Unknown Exception: Please check your email format or try again later.'}

        for mail_server in mail_servers:
            if result['code'] not in [0, 6]:
                break

            print('Attempting to connect to ' + str(mail_server.exchange)[:-1])
            try:
                server = smtplib.SMTP(str(mail_server.exchange)[:-1])
                #server.connect(str(mail_server.exchange)[:-1], 435)
                #server.login("aryanganotra7@gmail.com", "Arnidara123#")
            except Exception as ex:
                result = {'code':6, 'message': str(ex)}
                continue
            try:
                (code, msg) = server.helo("api.verifyleads.io")
                (code, msg) = server.docmd('MAIL FROM:', '<admin@verifyleads.io>')
                print(code,msg)
                if 200 <= code <= 299:
                    print('<{}>'.format(self.email))
                    (code, msg) = server.docmd('RCPT TO:', '<{}>'.format(self.email))
                    if code >= 500:
                        if code == 550 and ('blocked' or 'Blocked' in msg):
                            result = {'code':0, 'message': 'Cannot verify this email address because of some proxy errors.'}
                        else:
                            result = {'code':3, 'message': 'Mail server found for domain, but the email address is not valid.'}
                    elif code == 452:
                        result = {'code':0, 'message' : 'Too many requests'}
                    else:
                        server = smtplib.SMTP(str(mail_server.exchange)[:-1])
                        server.helo("api.verifyleads.io")
                        server.docmd('MAIL FROM:', '<dev@verifyleads.io>')
                        random_username = ''.join(random.sample(username,len(username))) +'07'
                        if(random_username.startswith('.')):
                            random_username += 'ar'
                        try_email = '<{}@{}>'.format(random_username, domain)
                        #try_email = '<{}@{}>'.format(str(uuid.uuid4())[:6], domain)
                        print("Checking for try email - ", try_email)
                        (code_bad_email, msg) = server.docmd('RCPT TO:', try_email)
                        print(code_bad_email, msg)
                        if code != code_bad_email and 200 <= code <= 299:
                            print(code)
                            result = {'code':1, 'message': 'Mail server indicates this is a valid email address'}
                        else:
                            print(code)
                            print(code_bad_email)
                            result = {"code":2, "message": 'Mail server found for domain, but this a catch-all domain. Email can be valid/invalid.'}
            except Exception as ex:
                try:
                    server.quit()
                except Exception:
                    pass

        result['email'] = self.email
        result['domain'] = domain 
        result['username'] = username 
        result['email'] = self.email
        print ('Done', result)
        return result

    def _get_domain_from_email_address(self,email_address):
            return re.search(r"([^@]+)", email_address), re.search(r"(?<=@)\[?([^\[\]]+)", email_address)
        


    # def __returnInvalidRegex(self):
    #     EMAIL_REGEX_INVALID = "Email address format is invalid. Please enter a valid email address."
    #     return json.dumps({'code':0, 'message': "Email address format is invalid. Please enter a valid email address."})
            