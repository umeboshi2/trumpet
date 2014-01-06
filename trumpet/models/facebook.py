from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import PickleType
from sqlalchemy import BigInteger


from sqlalchemy.orm import relationship, backref

from base import Base

# imports for populate()
import transaction
from sqlalchemy.exc import IntegrityError
from base import DBSession
from base import SerialBase

nametype = Unicode(100)
smalltxt = Unicode(25)
fb_primary = Column(BigInteger, primary_key=True)
fb_subprime = Column(BigInteger, ForeignKey('fb_json'), primary_key=True)

class FB_JSON(Base, SerialBase):
    __tablename__ = 'fb_json'
    id = fb_primary
    content = Column(PickleType)
    md5 = Column(smalltxt)
    updated = Column(DateTime)
    
    def __init__(self, id, content):
        self.id = id
        self.content = content

class FB_JSON_Post(Base, SerialBase):
    __tablename__ = 'fb_json_post'
    id = Column(nametype, primary_key=True)
    content = Column(PickleType)
    md5 = Column(smalltxt)
    updated = Column(DateTime)
    
    def __init__(self, id, content):
        self.id = id
        self.content = content
    
class FB_Person(Base, SerialBase):
    __tablename__ = 'fb_people'
    id = fb_subprime
    username = Column(nametype, unique=True)
    name = Column(Unicode(255))
    first_name = Column(nametype)
    last_name = Column(nametype)
    middle_name = Column(nametype)
    locale = Column(smalltxt)
    

    def __init__(self, id):
        self.id = id
        



