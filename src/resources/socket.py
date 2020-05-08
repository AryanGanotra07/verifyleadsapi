# from src.app import socketio
# from flask_socketio import SocketIO,send,emit


# @socketio.on("connect")
# def onConnect():
#     print("Connected")

# @socketio.on("json")
# def handleJson(msg):
#     execute(msg)
#     return None


# def execute(msg):
#     first_name = msg['first']
#     last_name = msg['last']
#     domain = msg['message']
#     from src.resources.Tasks import verifyEmail
#     for email in toList(first_name, last_name, domain):
#         emit("email-finder-result", "Executing-"+email)
#         response = verifyEmail.delay(email)
#         # if(response and response['code'] == 1):
#         #     emit("email-finder-result", "Valid")
#         # else:
#         #     emit("email-finder-result", "Invalid")
            
#         # if (result and result['code'] == 1):
#         #     send(result['email'])
#         #     break


# def toList(first, last, domain):
#     list = []

#     list.append(first[0] + '@' + domain)                 # f@example.com
#     list.append(first[0] + last + '@' + domain)          # flast@example.com
#     list.append(first[0] + '.' + last + '@' + domain)    # f.last@example.com
#     list.append(first[0] + '_' + last + '@' + domain)    # f_last@example.com
#     list.append(first[0] + '-' + last + '@' + domain)    # f-last@example.com
#     list.append(first + '@' + domain)                    # first@example.com
#     list.append(first + last + '@' + domain)             # firstlast@example.com
#     list.append(first + '.' + last + '@' + domain)       # first.last@example.com
#     list.append(first + '_' + last + '@' + domain)       # first_last@example.com
#     list.append(first + '-' + last + '@' + domain)       # first-last@example.com
#     list.append(first[0] + last[0] + '@' + domain)       # fl@example.com
#     list.append(first[0] + '.' + last[0] + '@' + domain) # f.l@example.com
#     list.append(first[0] + '-' + last[0] + '@' + domain) # f_l@example.com
#     list.append(first[0] + '-' + last[0] + '@' + domain) # f-l@example.com
#     list.append(first + last[0] + '@' + domain)          # fistl@example.com
#     list.append(first + '.' + last[0] + '@' + domain)    # first.l@example.com
#     list.append(first + '_' + last[0] + '@' + domain)    # fist_l@example.com
#     list.append(first + '-' + last[0] + '@' + domain)    # fist-l@example.com
#     list.append(last + '@' + domain)                     # last@example.com
#     list.append(last[0] + '@' + domain)                  # l@example.com

#     return(list)