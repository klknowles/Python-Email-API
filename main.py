from flask import Flask, request
from flask_restful import Api, Resource
from smtplib import SMTP_SSL, SMTP_SSL_PORT
import imaplib
import email
import requests
import json

app = Flask(__name__)
api = Api(app)
#your email
user = ''
#your password
passwd = ''
imap_url = 'imap.gmail.com'

class EmailInbox(Resource):
    def get(self):
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, passwd)
        mail.select("inbox")
        _, search_data = mail.search(None, 'UNSEEN')
        my_message = []
        for num in search_data[0].split():
            email_data = {}
            _, data = mail.fetch(num, '(RFC822)')
            _, b = data[0]
            email_message = email.message_from_bytes(b)
            for header in ['subject', 'to', 'from', 'date']:
                email_data[header] = email_message[header]
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()
                elif part.get_content_type() == "text/html":
                   html_body = part.get_payload(decode=True)
                   email_data['html_body'] = html_body.decode()
            my_message.append(email_data)
        return my_message

class EmailSearch(Resource):
    def get(self, emailadd):
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, passwd)
        mail.select("inbox")
        _, search_data = mail.search(None, 'FROM', emailadd)
        my_message = []
        for num in search_data[0].split():
            email_data = {}
            _, data = mail.fetch(num, '(RFC822)')
            _, b = data[0]
            email_message = email.message_from_bytes(b)
            for header in ['subject', 'to', 'from', 'date']:
                email_data[header] = email_message[header]
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()
                elif part.get_content_type() == "text/html":
                   html_body = part.get_payload(decode=True)
                   email_data['html_body'] = html_body.decode()
            my_message.append(email_data)
        return my_message

class EmailDeleteFrom(Resource):
    def get(self, emailadd):
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, passwd)
        mail.select("inbox")
        _, search_data = mail.search(None, 'FROM', emailadd)
        for num in search_data[0].split():
            _, msg = mail.fetch(num, "(RFC822)")
            mail.store(num, "+FLAGS", "\\Deleted")

        mail.expunge()
        mail.close()
        mail.logout()
        return {"message":"Email deleted!"}
#lists the email in the inbox that hasnt been read
api.add_resource(EmailInbox, "/inbox")
#liss the emails received from the adddress submitted
api.add_resource(EmailSearch, "/search/<string:emailadd>")
#deletes the emails received from the address submitted
api.add_resource(EmailDeleteFrom, "/delete/<string:emailadd>")
#api.add_resource(apiTags, "/apiquery")
if __name__ == "__main__":
    app.run(debug=True)
