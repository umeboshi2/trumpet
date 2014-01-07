#from cStringIO import StringIO
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
import transaction


from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid

from trumpet.models.base import DBSession
from trumpet.models.usergroup import User, Group, Password
from trumpet.models.usergroup import UserGroup




from trumpet.managers.admin.users import UserManager

from trumpet.security import encrypt_password

import colander
import deform



def deferred_choices(node, kw):
    choices = kw['choices']
    return deform.widget.SelectWidget(values=choices)

def make_select_widget(choices):
    return deform.widget.SelectWidget(values=choices)

class AddUserSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        title = 'User Name',
        )
    password = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5),
        widget=deform.widget.PasswordWidget(size=20),
        title = 'Password',
        )
    confirm = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5),
        widget=deform.widget.PasswordWidget(size=20),
        title = 'Confirm Password',
        )
    

class AddtoGroupSchema(colander.Schema):
    group = colander.SchemaNode(
        colander.Integer(),
        widget=deferred_choices,
        title='Add to Group',
        )

    
