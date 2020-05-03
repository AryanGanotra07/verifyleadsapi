import json
import smtplib
import dns.resolver
import dns.exception
import uuid
from src.verifier.regex_check import regex_check
import re


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
            username_domain = self._get_domain_from_email_address(self.email)
            username = username_domain[0]
            domain = username_domain[1]
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
                (code, msg) = server.helo('verifyleads.io')
                (code, msg) = server.docmd('MAIL FROM:', '<admin@verifyleads.io>')
                print(code,msg)
                if 200 <= code <= 299:
                    (code, msg) = server.docmd('RCPT TO:', '<{}>'.format(self.email))
                    if code >= 500:
                        print(code)
                        result = {'code':3, 'message': 'Mail server found for domain, but the email address is not valid'}
                    else:
                        (code_bad_email, msg) = server.docmd('RCPT TO:', '<{}@{}>'.format(str(uuid.uuid4()), domain))
                        if code != code_bad_email and 200 <= code <= 299:
                            print(code)
                            result = {'code':1, 'message': 'Mail server indicates this is a valid email address'}
                        else:
                            print(code)
                            print(code_bad_email)
                            result = {"code":2, "message": 'Mail server found for domain, but the server doesn\'t allow e-mail address verification'}
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
            return re.search(r"(?<=@)\[?([^\[\]]+)", email_address)
        


    # def __returnInvalidRegex(self):
    #     EMAIL_REGEX_INVALID = "Email address format is invalid. Please enter a valid email address."
    #     return json.dumps({'code':0, 'message': "Email address format is invalid. Please enter a valid email address."})
            