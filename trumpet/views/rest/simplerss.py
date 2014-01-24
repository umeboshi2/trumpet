from ConfigParser import ConfigParser
from StringIO import StringIO
from os.path import join as pjoin
import json
import time

from cornice.resource import resource, view
import feedparser


from trumpet.models.usergroup import User, Group, Password
from trumpet.models.usergroup import UserGroup

from trumpet.models.rssdata import Feed, FeedData

from trumpet.managers.simplerss import RssManager

from trumpet.security import encrypt_password

from trumpet.views.rest.base import BaseResource
    
# FIXME: this needs to be in manager
import transaction

# http://stackoverflow.com/questions/5505667/python-couchdb-cant-save-dict-created-from-feedparser-entry-no-attribute-rea
def make_json(obj):
    if isinstance(obj, time.struct_time):
        return {'__class__': 'time.asctime',
                '__value__': time.asctime(obj)}
    raise TypeError('No method to convert %s to JSON.' % repr(obj))

                

class BaseRSSResource(BaseResource):
    def __init__(self, request):
        super(BaseRSSResource, self).__init__(request)
        self.mgr = RssManager(request.db)
        
        
        
basepath = '/rest/simplerss'

@resource(collection_path=pjoin(basepath, 'feeds'),
          path=pjoin(basepath, 'feeds', '{id}'))
class FeedResource(BaseRSSResource):
    dbmodel = Feed

    def collection_get(self):
        feeds = self.mgr.list_feeds()
        feeds = [f.serialize() for f in feeds]
        return dict(data=feeds, result='success')

    def collection_post(self):
        name = self.request.json['name']
        url = self.request.json['url']
        obj = self.mgr.add_feed(name, url)
        data = dict(obj=obj.serialize(), result='success')
        return data
        
    def collection_put(self):
        if self.request.json and 'id' in self.request.json:
            j = self.request.json
            id = j['id']
            name = j['name']
            url = j['url']
            feed = self.mgr.update_feed_info(id, name, url)
            return dict(obj=feed.serialize(), result='success')
        else:
            self.mgr.update_feeds()
            return dict(result='success')

    def put(self):
        id = self.request.matchdict['id']
        name = self.request.json['name']
        url = self.request.json['url']
        print 'NAME', name
        raise RuntimeError, "Not implemented"
    
        
    

              
              
@resource(path=pjoin(basepath, 'feeds', '{id}', 'feeddata'))
class FeedDataResource(BaseRSSResource):
    dbmodel = FeedData

    def get(self):
        id = int(self.request.matchdict['id'])
        feed = self.mgr.view_latest_feed(id)
        data = dict(feed['rss'].content)
        data['id'] = id
        j = json.dumps(data, default=make_json)
        return json.loads(j)
    
        

    def put(self):
        id = int(self.request.matchdict['id'])
        return self.mgr.update_feed(id)
    


