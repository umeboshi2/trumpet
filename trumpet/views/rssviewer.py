from datetime import datetime, timedelta


import feedparser

import transaction
from formencode.htmlgen import html
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render


from trumpet.models.base import DBSession
from trumpet.models.rssdata import Feed, FeedData

from base import BaseViewer

from menus import BaseMenu

import colander
import deform


class AddFeedSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=1, max=85),
        title='Feed Name',
        description='Please enter the name of the feed',
        )
    url = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=7, max=255),
        title='Feed URL',
        description='Please enter the URL of the feed',
        )
    
    
def prepare_main_data(request):
    layout = request.layout_manager.layout
    layout.title = 'RSS Viewer Page'
    layout.header = 'RSS Viewer Page'
    layout.subheader = ''
    layout.content = request.matchdict['context']
    layout.footer = str(request.params)


class MainViewer(BaseViewer):
    def __init__(self, request):
        super(MainViewer, self).__init__(request)
        # make dispatch table
        self._dispatch_table = dict(addfeed=self.add_feed,
                                    listfeeds=self.list_feeds,
                                    viewfeed=self.view_feed,
                                    updatefeeds=self.update_feeds)
        self.context = request.matchdict['context']
        self._view = self.context
        self.dbsession = DBSession()
        prepare_main_data(self.request)
        # make left menu
        entries = []
        url = self.url(context='listfeeds', feed=None)
        entries.append(('View Feeds', url))
        url = self.url(context='addfeed', feed=None)
        entries.append(('Add Feed', url))
        url = self.url(context='updatefeeds', feed=None)
        entries.append(('Update Feeds', url))
        if self.context in ['viewfeed']:
            url = self.url(context='deletefeed',
                           feed=self.request.matchdict['feed'])
            entries.append(('Delete Feed', url))
        header = 'RSS View Menu'        
        self.layout.ctx_menu.set_new_entries(entries, header=header)
        self.dispatch()

    def add_feed(self):
        schema = AddFeedSchema()
        form = deform.Form(schema, buttons=('submit',))
        #form = AddFeedForm(self.request.POST)
        #form.add_submit("Add Feed")
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            self.layout.subheader = 'submitted'
            controls = self.request.POST.items()
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            # form is valid, add to database
            with transaction.manager:
                feed = Feed(data['name'], data['url'])
                self.request.db.add(feed)
        else:
            rendered = form.render()
            self.layout.content = rendered
            self.layout.subheader = 'Please add a Feed'
        
    def _get_latest_feed(self, feed):
        "gets latest feed in database"
        query = self.dbsession.query(FeedData).filter_by(feed_id=feed.id)
        return query.order_by(desc(FeedData.retrieved)).first()
        
    def update_feeds(self):
        query = self.dbsession.query(Feed)
        for feed in query.all():
            data = self._get_latest_feed(feed)
            data = self._update_feed(feed, data)
        self.layout.content = '<h1>Feeds Updated</h1>'
        
    def list_feeds(self):
        ulist = html.ul()
        query = self.dbsession.query(Feed)
        for feed in query.all():
            vfeed = self.request.route_url('rssviewer',
                                           context='viewfeed', feed=feed.id)
            anchor = html.a(feed.name, href=vfeed)
            item = html.li(anchor)
            ulist.append(item)
        self.layout.content = unicode(ulist)

    def view_feed(self):
        feed_id = self.request.matchdict['feed']
        feed = self.dbsession.query(Feed).filter_by(id=feed_id).one()
        data = self._get_latest_feed(feed)
        self._update_feed(feed, data)
        env = dict(feed=feed, rss=self._get_latest_feed(feed))
        template = 'trumpet:templates/rss_entries.mako'
        self.layout.content = render(template, env, request=self.request)
        
    def _get_new_feed_data(self, feed):
        data = feedparser.parse(feed.url)
        with transaction.manager:
            fdata = FeedData(feed.id, data)
            self.dbsession.add(fdata)
        return data
    
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
                msg = 'Still waiting %s seconds left.'
                self.layout.subheader = msg % diff
        else:
            data = self._get_new_feed_data(feed)
        return data
