# email_utils.py
from flask_mail import Message
from extensions import mail


# def send_email(subject, sender, recipients, text_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_attachment=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if html_attachment:
        msg.attach("message.html", "text/html; charset=UTF-8",
                   html_attachment.encode('utf-8'))

    mail.send(msg)
