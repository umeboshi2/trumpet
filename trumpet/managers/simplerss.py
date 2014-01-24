import os
from datetime import datetime, timedelta
from zipfile import ZipFile
from StringIO import StringIO
import csv
from io import BytesIO

import feedparser

import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from sqlalchemy import func

from trumpet.models.sitecontent import SiteText

from trumpet.models.rssdata import Feed, FeedData


class RssManager(object):
    def __init__(self, session):
        self.session = session
    
    def add_feed(self, name, url):
        with transaction.manager:
            feed = Feed(name, url)
            self.session.add(feed)
        return self.session.merge(feed)

    def update_feed_info(self, feed_id, name, url):
        with transaction.manager:
            feed = self.session.query(Feed).get(feed_id)
            if feed is not None:
                feed.name = name
                feed.url = url
                self.session.add(feed)
        return self.session.merge(feed)
    
    def _get_latest_feed(self, feed):
        "gets latest feed in database"
        query = self.session.query(FeedData).filter_by(feed_id=feed.id)
        return query.order_by(desc(FeedData.retrieved)).first()
        
    def _get_new_feed_data(self, feed):
        data = feedparser.parse(feed.url)
        with transaction.manager:
            fdata = FeedData(feed.id, data)
            self.session.add(fdata)
        return self.session.merge(fdata)
    
    
    def _update_feed(self, feed, data):
        "take the lasted data row from rssdata and see if need to update"
        if data is not None:
            # 90 minute limit
            limit = timedelta(0, 0, 0, 0, 90)
            now = datetime.now()
            if now > data.retrieved + limit:
                self._get_new_feed_data(feed)
            else:
                diff = (data.retrieved + limit) - now
        else:
            data = self._get_new_feed_data(feed)
        return data

    def update_feed(self, feed_id):
        feed = self.session.query(Feed).get(feed_id)
        if feed is None:
            raise RuntimeError, 'No feed to update'
        data = self._get_latest_feed(feed)
        data = self._update_feed(feed, data)
        return data
    
    def update_feeds(self):
        query = self.session.query(Feed)
        for feed in query.all():
            data = self._get_latest_feed(feed)
            data = self._update_feed(feed, data)
          
    def list_feeds(self):
        query = self.session.query(Feed)
        return query.all()

    def view_latest_feed(self, feed_id):
        feed = self.session.query(Feed).filter_by(id=feed_id).one()
        data = self._get_latest_feed(feed)
        self._update_feed(feed, data)
        env = dict(feed=feed, rss=self._get_latest_feed(feed))
        return env
