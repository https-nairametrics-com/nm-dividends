from django.core.mail import EmailMessage
import string
import random

import threading
from .models import Comment


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()


# Generate Comment Slug


def transaction_generator(size=8, chars=string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    # Check if ID exist in database
    try:
        order_gen = Comment.objects.get(slug=the_id)
        transaction_generator
    except Comment.DoesNotExist:
        return the_id
