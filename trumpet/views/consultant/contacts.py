import string

import colander
import deform
import vobject

from sqlalchemy.exc import IntegrityError

from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound


from trumpet.managers.consultant.contacts import ContactManager



phone_re = '\((?P<areacode>[1-9][0-9][0-9])\)-(?P<prefix>[0-9][0-9][0-9])-(?P<suffix>[0-9][0-9][0-9][0-9])'
letters = string.ascii_letters[26:]

class AddContactSchema(colander.Schema):
    firstname = colander.SchemaNode(
        colander.String(),
        title = 'First Name',
        )
    lastname = colander.SchemaNode(
        colander.String(),
        title = 'Last Name',
        missing=colander.null,
        )
    email = colander.SchemaNode(
        colander.String(),
        validator=colander.Email(),
        title='Email Address',
        missing=colander.null,
        )
    phone = colander.SchemaNode(
        colander.String(),
        title='Phone Number',
        widget=deform.widget.TextInputWidget(mask='(999)-999-9999',
                                      mask_placeholder='0'),
        missing=colander.null,
        )

