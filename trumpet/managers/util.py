import os
from datetime import datetime, timedelta
import smtplib
from email.MIMEText import MIMEText

import vobject

from trumpet.models.usergroup import User


def convert_range_to_datetime(start, end):
    "start and end are timestamps"
    start = datetime.fromtimestamp(float(start))
    end = datetime.fromtimestamp(float(end))
    return start, end


def parse_vcard_object(card):
    firstname = card.n.value.given
    if not firstname:
        firstname = None
    lastname = card.n.value.family
    email = None
    if hasattr(card, 'email'):
        email = card.email.value
        if not email:
            email = None
    phone = None
    if hasattr(card, 'tel'):
        phone = card.tel.value
        if not phone:
            phone = None
    return firstname, lastname, email, phone


def make_vcard(contact):
    card = vobject.vCard()
    card.add('n')
    card.n.value = vobject.vcard.Name(family=contact.lastname,
                                      given=contact.firstname)
    card.add('fn')
    fullname = contact.lastname
    if contact.firstname:
        fullname = '%s %s' % (contact.firstname, contact.lastname)
    card.fn.value = fullname
    card.add('email')
    card.email.type_param = 'INTERNET'
    if contact.email is not None:
        card.email.value = contact.email
    card.add('tel')
    card.tel.type_param = 'WORK'
    if contact.phone is not None:
        card.tel.value = contact.phone
    return card


def make_email_message(subject, message, sender, receiver):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    return msg


def send_email_through_smtp_server(settings, message, sender, receiver):
    prefix = 'smtp.'
    server = settings[prefix + 'server']
    port = int(settings[prefix + 'port'])
    login = settings[prefix + 'login']
    password = settings[prefix + 'password']
    server = smtplib.SMTP(server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login, password)
    msg = message.as_string()
    server.sendmail(sender, receiver, msg)
    server.close()
