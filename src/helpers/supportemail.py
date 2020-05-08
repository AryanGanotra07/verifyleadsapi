import requests
import json


zohoApi = "https://mail.zoho.in/api/accounts/592133000000002002/messages"

def get_html_content(name):
    return "<html><head><title>Verify Leads</title><style>body {background-color: rgb(255,160,122);text-align: center;color: black;font-family: Arial, Helvetica, sans-serif;}a.button {-webkit-appearance: button;-moz-appearance: button;margin-top:40px;appearance: button;background-color : #ff5722;text-decoration: none;color: white;padding:30px; }</style></head><body><div style=\" background-color:white; padding:20px;\"><img src=\"https://media-exp1.licdn.com/dms/image/C560BAQH908kZrXga1A/company-logo_200_200/0?e=1596672000&v=beta&t=Tgt-p5pXByxqUQkuw3yDU6fgc9xW8CJdOEnYqKKEvdk\" alt=\"Avatar\"><h1>Hello " + name + "</h1><h3>Thank you for your query.</h3><h4>We will get back to you shortly</h4><p style=\"margin-bottom:60px\">Verify and Find Professional Emails with over 98% Accuracy.</p><a href=\"https://verifyleads.io\" class=\"button\">VERIFYLEADS.IO</a></div></body></html>"


def sendEmail(data):
    message = get_html_content(data['name'])
    email = data['email']
    data =  {
   "fromAddress": "admin@verifyleads.io",
   "toAddress": email,
   "ccAddress": "",
   "bccAddress": "",
   "subject": "Support Ticket @verifyleads.io",
   "content": message,
   "askReceipt" : "yes"
}
    headers = {'Content-Type': 'application/json', 'Authorization' : '8e989e1483f989e32897b5ad36e24a91'}

    data = json.dumps(data)
    resp = requests.post(zohoApi, data = data, headers = headers)
    print(resp.content)