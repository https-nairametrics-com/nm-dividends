from django.core.mail import EmailMessage
import string
import random

import threading
from .models import User
from investment.models import Investors


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


# Generate referral code
def referral_generator(size=7, chars=string.ascii_lowercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))

    # Check if ID exist in database
    try:
        order_gen = User.objects.get(referral_code=the_id)
        referral_generator
    except User.DoesNotExist:
        return the_id

# Generate transaction ID


def transaction_generator(size=13, chars=string.ascii_lowercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    # Check if ID exist in database
    try:
        order_gen = User.objects.get(referral_code=the_id)
        transaction_generator
    except User.DoesNotExist:
        return the_id

# Generate transaction ID


def serial_investor(size=13, chars=string.ascii_lowercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    # Check if ID exist in database
    try:
        order_gen = Investors.objects.get(serialkey=the_id)
        investor_slug
    except Investors.DoesNotExist:
        return the_id

# Generate investor ID


def investor_slug(size=6, chars=string.ascii_lowercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    # Check if ID exist in database
    try:
        order_gen = Investors.objects.get(slug=the_id)
        investor_slug
    except Investors.DoesNotExist:
        return the_id

# Generate username  ID


def username_generator(size=4, chars=string.ascii_lowercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    # Check if ID exist in database
    try:
        order_gen = User.objects.get(referral_code=the_id)
        username_generator
    except User.DoesNotExist:
        return the_id


def slug_generator(size=4, chars=string.ascii_lowercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    # Check if ID exist in database
    return the_id
