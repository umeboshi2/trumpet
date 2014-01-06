from datetime import datetime

import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import PickleType


from sqlalchemy.orm import relationship, backref

from base import Base


from base import DBSession, SerialBase
from sqlalchemy.exc import IntegrityError


class Feed(Base, SerialBase):
    __tablename__ = 'rssfeeds'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), unique=True)
    url = Column(Unicode(255), unique=True)

    def __init__(self, name, url):
        self.name = name
        self.url = url


class FeedData(Base, SerialBase):
    __tablename__ = 'rssdata'
    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey('rssfeeds.id'))
    content = Column(PickleType)
    retrieved = Column(DateTime, default=datetime.now)

    def __init__(self, feed_id, content):
        self.feed_id = feed_id
        self.content = content

class FeedEntry(Base, SerialBase):
    __tablename__ = 'rss_entries'
    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey('rssfeeds.id'))
    entry_id = Column(Unicode, unique=True)
    published = Column(DateTime)
    
FeedData.feed = relationship(Feed)

FEEDS = [
    'google_us_news|http://news.google.com/news?ned=us&topic=n&output=rss',
    'google_debian_news|http://news.google.com/news?q=debian&output=rss',
    'google_top_news|http://news.google.com/news?ned=us&topic=h&output=rss',
    'CNN Top Stories|http://rss.cnn.com/rss/cnn_topstories.rss',
    'New York TImes|http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'Science Daily|http://www.sciencedaily.com/newsfeed.xml',
    'Science Daily:Strange Science|http://www.sciencedaily.com/rss/strange_science.xml',
    'Planet KDE|http://planetkde.org/rss20.xml',
    'Planet Python|http://planet.python.org/rss20.xml',
    'reddit|http://www.reddit.com/.rss',
    'reddit  r/linux|http://www.reddit.com/r/linux/.rss',
    'reddit  r/debian|http://www.reddit.com/r/debian/.rss',
    'reddit  r/python|http://www.reddit.com/r/Python/.rss',
    'archive.org|http://archive.org/services/collection-rss.php',
    ]


def populate_feeds():
    session = DBSession()
    feeds = [f.split('|') for f in FEEDS]
    with transaction.manager:
        for name, url in feeds:
            f = Feed(name, url)
            session.add(f)
