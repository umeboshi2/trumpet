from ConfigParser import ConfigParser
from StringIO import StringIO

from sqlalchemy import Column
from sqlalchemy import Integer, Boolean
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import ForeignKey
from sqlalchemy import PickleType
from sqlalchemy import DateTime


from sqlalchemy.orm import relationship

from chert.alchemy import Base, SerialBase

# imports for populate()
import transaction
from sqlalchemy.exc import IntegrityError
from base import DBSession


class CeleryTask(Base, SerialBase):
    __tablename__ = 'celery_taskmeta'
    id = Column(Integer, primary_key=True, nullable=False)
    task_id = Column(Unicode(255))
    status = Column(Unicode(50))
    result = Column(PickleType)
    date_done = Column(DateTime)
    traceback = Column(UnicodeText)
