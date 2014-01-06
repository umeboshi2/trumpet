import hashlib
from datetime import datetime
import urlparse

import transaction
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render

from facebook import GraphAPI
from facebook import GraphAPIError

from haberdashery.resources import fbook_js

from trumpet.models.facebook import FB_JSON, FB_Person
from trumpet.models.facebook import FB_JSON_Post

from trumpet.fbauth import get_access_token

from base import NotFound, prepare_layout
from base import BaseViewer
from menus import BaseMenu

def parse_next_page_url(url):
    parsed = urlparse.urlparse(url)
    data = urlparse.parse_qs(parsed.query)
    args = {}
    for k, lv in data.items():
        args[k] = lv[0]
    parsed.args = args
    return parsed

    

def prepare_main_data(request):
    layout = request.layout_manager.layout
    layout.title = 'Facebook Trumpet'
    layout.header = 'Facebook'
    menu = layout.ctx_menu
    menu.set_header('Main Menu')
    url = request.route_url('fb', context='foo', id='bar')
    menu.append_new_entry('main', url)
    url = request.route_url('fb', context='listobjs', id=None)
    menu.append_new_entry('list objects', url)
    url = request.route_url('fb', context='listfriends', id=None)
    menu.append_new_entry('list friends', url)
    url = request.route_url('fb', context='newsfeed', id=None)
    menu.append_new_entry('NewsFeed', url)
    fbook_js.need()
    
newsfeed_query = "SELECT post_id, actor_id, target_id, message FROM stream WHERE filter_key in (SELECT filter_key FROM stream_filter WHERE uid=me() AND type='newsfeed') AND is_hidden = 0"
newsfeed_query2 = "SELECT post_id, type, actor_id, target_id, message, description, action_links, app_data, comments, created_time FROM stream where filter_key='others' or filter_key='owner' LIMIT 75"
newsfeed_query3 = "SELECT post_id FROM stream where filter_key='others' or filter_key='owner' LIMIT 25"


class FBViewer(BaseViewer):
    def __init__(self, request):
        super(FBViewer, self).__init__(request)
        prepare_main_data(self.request)
        self.token = get_access_token()
        self.graph = GraphAPI(self.token)
        self.route = self.request.matched_route.name
        if self.route == 'fbget':
            id = self.request.matchdict['id']
            self.get_object(id)
            return
        self._cntxt_meth = dict(
            listobjs=self.view_objects,
            listfriends=self.view_friends,
            newsfeed=self.view_newsfeed)
        self.context = self.request.matchdict['context']
        
        # dispatch context request
        if self.context in self._cntxt_meth:
            self._cntxt_meth[self.context]()
        else:
            msg = 'Undefined Context: %s' % self.context
            self.layout.content = '<b>%s</b>' % msg

    def add_json_post(self, identifier, content):
        with transaction.manager:
            fbjson = FB_JSON_Post(identifier, content)
            fbjson.updated = datetime.now()
            self.request.db.add(fbjson)
        fbjson = self.request.db.merge(fbjson)
        return fbjson

    def get_newsfeed_from_fb(self, offset=0):
        postlist = self.graph.fql(newsfeed_query3)
        for jpost in postlist:
            post_id = jpost['post_id']
            fbjson = self.request.db.query(FB_JSON_Post).get(post_id)
            if fbjson is None:
                try:
                    post = self.graph.get_object(post_id)
                except GraphAPIError:
                    continue
                fbjson = self.add_json_post(post_id, post)
            

    def view_newsfeed(self):
        #self.get_newsfeed_from_fb()
        #self.layout.content = '<h1>News Retrieved</h1>'
        posts = self.request.db.query(FB_JSON_Post).all()
        template = 'trumpet:templates/fb_newsfeed.mako'
        env = dict(posts=posts)
        content = render(template, env, request=self.request)
        self.layout.content = content
        
    def view_newsfeed2(self):
        
        content = ''
        for post_id in postids:
            try:
                post = self.graph.get_object(post_id)
            except GraphAPIError:
                post = '<h2>========|%s|========</h2>' % post_id
            posts.append(post)
            content += '<p>%s</p><hr>' % post
        self.layout.content = content
        
    def view_objects(self):
        #self.get_all_friends_from_fb()
        #news = self.graph.fql(newsfeed_query2)
        #import pdb;pdb.set_trace()
        objects = self.request.db.query(FB_JSON).all()
        data = ''
        tb = self.graph.fql(newsfeed_query)
        #import pdb;pdb.set_trace()
        for obj in objects:
            href = 'https://graph.facebook.com/%d/picture' % obj.id
            data += '<img class="fbfriend" src="%s">%s</img>\n' % (href, obj.id)
            data += '<p>%s</p>\n' % obj.content['name']
        self.layout.content = data

    def view_friends(self):
        people = self.request.db.query(FB_Person).all()
        if not people:
            self.get_all_friends_from_fb()
            self.layout.content = 'Friends updated from facebook'
            return
        template = 'trumpet:templates/fb_friends.mako'
        env = dict(people=people)
        content = render(template, env, request=self.request)
        self.layout.content = content
        
    def get_all_friends_from_fb(self):
        friends = self.graph.get_connections('me', 'friends')
        for friend in friends['data']:
            id = friend['id']
            print "friend", friend
            print "id", id
            
            fbjson = self._get_object(id)
            print "adding", fbjson.content['name']
            self.add_friend(fbjson.id, fbjson.content)
            
    def add_friend(self, identifier, content):
        with transaction.manager:
            friend = FB_Person(identifier)
            for k in ['username', 'name', 'first_name', 'middle_name',
                      'last_name', 'locale']:
                if k in content:
                    setattr(friend, k, content[k])
            self.request.db.add(friend)
        return self.request.db.merge(friend) 
        
    def add_object(self, identifier, content):
        transaction.begin()
        fbjson = FB_JSON(identifier, content)
        fbjson.updated = datetime.now()
        self.request.db.add(fbjson)
        transaction.commit()
        fbjson = self.request.db.merge(fbjson)
        return fbjson

    def _get_object(self, identifier):
        fbjson = self.request.db.query(FB_JSON).get(identifier)
        #print "fbjson is", type(fbjson), fbjson
        if fbjson is None:
            content = self.graph.get_object(identifier)
            fbjson = self.add_object(identifier, content)
        return fbjson
        
    def get_object(self, identifier):
        self.response = self._get_object(identifier).content
    
