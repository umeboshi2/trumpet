from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode, UnicodeText, Text
from sqlalchemy import ForeignKey
from sqlalchemy import Date, Time, DateTime
from sqlalchemy import Enum


from sqlalchemy.orm import relationship, backref

from base import Base

from base import DBSession
import transaction


#######################################################
# wiki pages
#######################################################
class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    content = Column(Text)

    def __init__(self, name, content):
        self.name = name
        self.content = content


class WikiPage(Base):
    __tablename__ = 'wiki_pages'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    content = Column(Text)
    created = Column(DateTime)
    modified = Column(DateTime)


def populate_wiki():
    session = DBSession()
    with transaction.manager:
        page = Page('FrontPage', 'This is the front page.')
        session.add(page)

