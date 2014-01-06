from ConfigParser import ConfigParser
from StringIO import StringIO

from sqlalchemy import Column
from sqlalchemy import Integer, Boolean
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import ForeignKey


from sqlalchemy.orm import relationship

from base import Base

# imports for populate()
import transaction
from sqlalchemy.exc import IntegrityError
from base import DBSession


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(50), unique=True)
    email = Column(Unicode(50), unique=True)
    active = Column(Boolean, default=True)
    pw = relationship('Password', uselist=False)
    
    def __init__(self, username=None):
        self.username = username

    def serialize(self):
        data = dict(id=self.id, username=self.username,
                    email=self.email, active=self.active)
        return data
    
    def __repr__(self):
        return self.username

    def get_groups(self):
        return [g.name for g in self.groups]

    
class UserConfig(Base):
    __tablename__ = 'user_config'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    text = Column(UnicodeText)

    def __init__(self, user_id=None, text=None):
        self.user_id = user_id
        self.text = text

    def serialize(self):
        return dict(user_id=self.user_id, text=self.text)

    def get_config(self):
        c = ConfigParser()
        c.readfp(StringIO(self.text))
        return c

    def set_config(self, config):
        cfile = StringIO()
        config.write(cfile)
        cfile.seek(0)
        text = cfile.read()
        self.text = text
        #return self
    
class Password(Base):
    __tablename__ = 'passwords'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    password = Column(Unicode(150))

    def __init__(self, user_id=None, password=None):
        self.user_id = user_id
        self.password = password

    def serialize(self):
        return dict(user_id=self.user_id, password=self.password)
    
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True)

    def __init__(self, name=None):
        self.name = name

    def serialize(self):
        return dict(id=self.id, name=self.name)
    
class UserGroup(Base):
    __tablename__ = 'group_user'
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    def __init__(self, gid=None, uid=None):
        self.group_id = gid
        self.user_id = uid

    def serialize(self):
        return dict(group_id=self.group_id, user_id=self.user_id)
    

User.groups = relationship(Group, secondary='group_user')
User.config = relationship(UserConfig, uselist=False, lazy='subquery')
Group.users = relationship(User, secondary='group_user')



def populate_groups():
    session = DBSession()
    groups = ['admin', 'editor', 'manager']
    for gname in groups:
        try:
            with transaction.manager:
                group = Group(gname)
                session.add(group)
        except IntegrityError:
            pass
            

def populate_users(admin_username):
    from trumpet.security import encrypt_password
    session = DBSession()
    with transaction.manager:
        users = [admin_username]
        # Using id_count to presume
        # the user's id, which should work
        # when filling an empty database.
        id_count = 0
        for uname in users:
            id_count += 1
            user = User(uname)
            password = encrypt_password(uname)
            session.add(user)
            pw = Password(id_count, password)
            session.add(pw)

def populate_usergroups():
    session = DBSession()
    with transaction.manager:
        admins = [(1, 1)]  # admin user should be 1
        ulist = admins
        for gid, uid in ulist:
            row = UserGroup(gid, uid)
            session.add(row)


def populate(admin_username):
    # populate groups
    try:
        populate_groups()
    except IntegrityError:
        transaction.abort()
    # populate users
    try:
        populate_users(admin_username)
    except IntegrityError:
        transaction.abort()
    # add users to groups
    try:
        populate_usergroups()
    except IntegrityError:
        transaction.abort()
