import json
import smtplib
import dns.resolver
import dns.exception
import uuid
from src.verifier.regex_check import regex_check, regex_check_name, regex_check_domain
import re
import socket
import random


EMAIL_INVALID_RESULT = {'code':0, 'message': "Email address format is invalid. Please enter a valid email address."}
class EmailVerifier:

    

    def __init__(self, email) :
        self.email = email
        
    @staticmethod
    def verify(email):
        
        result = {'code':0, 'message': "Unknown exception occurred. Please try again later."}
        regexVerified = regex_check(email)
        if (regexVerified != True):
            print("Invalid regex")
            return EMAIL_INVALID_RESULT
        username, domain = "", ""
        try:
            username_r, domain_r = EmailVerifier.get_domain_from_email_address(email)
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
                (code, msg) = server.helo("ubtpro.com")
                (code, msg) = server.docmd('MAIL FROM:', '<contact@ubtpro.com>')
                print(code,msg)
                if 200 <= code <= 299:
                    print('<{}>'.format(email))
                    (code, msg) = server.docmd('RCPT TO:', '<{}>'.format(email))
                    if code >= 500:
                        print(code, msg)
                        if code == 550 and ('5.4.1' in str(msg)):
                            result = {'code':0, 'message': 'Cannot verify this email address because of some proxy errors.'}
                        else:
                            result = {'code':3, 'message': 'Mail server found for domain, but the email address is not valid.'}
                    elif code == 452:
                        result = {'code':0, 'message' : 'Too many requests'}
                    else:
                        server = smtplib.SMTP(str(mail_server.exchange)[:-1])
                        server.helo("ubtpro.com")
                        server.docmd('MAIL FROM:', '<support@ubtpro.com>')
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
                    break
            except Exception as ex:
                print(ex)
                try:
                    server.quit()
                except Exception:
                    pass

        result['email'] = email
        result['domain'] = domain 
        result['username'] = username 
        result['email'] = email
        print ('Done', result)
        return result
    
    @staticmethod
    def get_domain_from_email_address(email_address):
            return re.search(r"([^@]+)", email_address), re.search(r"(?<=@)\[?([^\[\]]+)", email_address)

    @staticmethod
    def emailFinder(f_name,l_name, domain):
        f_name_regex_verified = regex_check_name(f_name)
        l_name_regex_verified = regex_check_name(l_name)
        domain_regex_verified = regex_check_domain(domain)
        if (f_name_regex_verified != True):
            return {"code" : 0, "message" : "Please enter valid first name"}
        if (l_name_regex_verified != True):
            return {"code" : 0, "message" : "Please enter valid last name"}
        if (domain_regex_verified != True):
            return {"code" : 0, "message" : "Please enter valid domain name"}
        for email in EmailVerifier._getList(f_name, l_name, domain):
            response = EmailVerifier.verify(email)
            if (response['code'] == 1 or response['code'] == 2):
                response['f_name'] = f_name
                response['l_name'] = l_name
                return response
            if (response['code'] == 0):
                return response
        return {"code" : 0, "message" : "Sorry, can't lookup any."} , 201
                

    @staticmethod
    def _getList(first, last, domain):
        list = []
        list.append(first + '.' + last + '@' + domain)       # first.last@example.com
        list.append(first[0] + last + '@' + domain)          # flast@example.com
        list.append(first + '@' + domain)                    # first@example.com
        list.append(first + last + '@' + domain)             # firstlast@example.com
        list.append(first + last[0] + '@' + domain)          # fistl@example.com
        list.append(last + '@' + domain)                     # last@example.com
        list.append(first + '_' + last + '@' + domain)       # first_last@example.com
        list.append(last + first[0] + '@' + domain)       # lastf@example.com
        list.append(first[0] + '_' + last + '@' + domain)    # f_last@example.com
        list.append(first + '-' + last + '@' + domain)       # first-last@example.com
        #list.append(first[0] + last[0] + '@' + domain)       # fl@example.com
        #list.append(first[0] + '.' + last[0] + '@' + domain) # f.l@example.com
        #list.append(first[0] + '-' + last[0] + '@' + domain) # f_l@example.com
        #list.append(first[0] + '-' + last[0] + '@' + domain) # f-l@example.com
        list.append(first + '.' + last[0] + '@' + domain)    # first.l@example.com
        list.append(first + '_' + last[0] + '@' + domain)    # fist_l@example.com
        list.append(first + '-' + last[0] + '@' + domain)    # fist-l@example.com
       # list.append(last[0] + '@' + domain)                  # l@example.com

        return(list)
        


    # def __returnInvalidRegex(self):
    #     EMAIL_REGEX_INVALID = "Email address format is invalid. Please enter a valid email address."
    #     return json.dumps({'code':0, 'message': "Email address format is invalid. Please enter a valid email address."})
            