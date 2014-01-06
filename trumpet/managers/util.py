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


def datetime_from_pdf_filename(filename):
    dtstring = filename.split('_')[0]
    year = int(dtstring[0:2]) + 2000
    month = int(dtstring[2:4])
    day = int(dtstring[4:6])
    hour = int(dtstring[6:8])
    minutes = int(dtstring[8:10])
    seconds = int(dtstring[10:12])
    return datetime(year, month, day, hour, minutes, seconds)

def get_scanned_filenames(directory):
    filenames = os.listdir(directory)
    now = datetime.now()
    prefix = str(now.year - 2000)
    filenames = (f for f in filenames if f.startswith(prefix))
    filenames = (f for f in filenames if len(f) == 21)
    filenames = (f for f in filenames if f.index('_') == 12)
    return filenames


def get_scanned_pdfs(directory):
    filenames = get_scanned_filenames(directory)
    dts = [datetime_from_pdf_filename(f) for f in filenames]
    content = ''
    for f in filenames:
        fp = os.path.join(directory, f)
        content += file(fp).read()
    return len(content)/ 1024.0 / 1024.0

def get_scanned_pdfs_request(request):
    settings = request.registry.settings
    dirname = settings['consultant.scans.directory']
    return get_scanned_pdfs(dirname)


def get_regular_users(request):
    users = request.db.query(User).all()
    skey = 'trumpet.admin_username'
    admin_username = request.registry.settings.get(skey, 'admin')
    return [u for u in users if u.username != admin_username]
