from pyramid.response import Response

from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from trumpet.models.sitecontent import SiteImage
from trumpet.models.sitecontent import SiteCSS, SiteJS
from trumpet.models.sitecontent import SiteTemplate

FILETYPE_MAP = dict(css=SiteCSS, js=SiteJS,
                    ejs=SiteTemplate, image=SiteImage,
                    thumb=SiteImage)
CONTENT_TYPE_MAP = dict(image='image/jpeg', thumb='image/jpeg',
                        css='text/css', js='text/javascript',
                        ejs='text/javascript')

# FIXME: update this to use BasicView
class BlobViewer(object):
    def __init__(self, request):
        self.request = request
        self.content = {}
        self.filetype = None
        if 'filetype' in self.request.matchdict:
            self.filetype = self.request.matchdict['filetype']

        self.db = self.request.db

        # make dispatch table
        self._viewmap = dict(
            image=self.get_image,
            thumb=self.get_thumb,
            css=self.get_css,
            js=self.get_js,
            ejs=self.get_ejs,)

        # implement search first
        # if 'id' is search
        id = self.request.matchdict['id']
        if id == 'search':
            self.search()
        else:
            # dispatch filetype request
            if self.filetype in self._viewmap:
                self._viewmap[self.filetype]()
            else:
                self.content = HTTPNotFound()
            
    def __call__(self):
        return self.content

    def _get_db_object(self, id):
        dbmodel = FILETYPE_MAP[self.filetype]
        return self.db.query(dbmodel).get(id)
    
    def _get_object_content(self, obj):
        att = 'content'
        if self.filetype == 'thumb':
            att = 'thumbnail'
        return getattr(obj, att)

    def _make_response(self, body):
        content_type = CONTENT_TYPE_MAP[self.filetype]
        response = Response(body=body,
                            content_type=content_type)
        self.content = response

    def _get_content(self, id):
        obj = self._get_db_object(id)
        content = self._get_object_content(obj)
        self._make_response(content)
    
    def get_image(self):
        id = self.request.matchdict['id']
        self._get_content(id)
    
    def get_thumb(self):
        id = self.request.matchdict['id']
        self._get_content(id)
    
    def get_css(self):
        id = self.request.matchdict['id']
        self._get_content(id)
    
    def get_js(self):
        id = self.request.matchdict['id']
        self._get_content(id)

    def get_ejs(self):
        id = self.request.matchdict['id']
        self._get_content(id)
        
    def search(self):
        name = self.request.GET['name']
        dbmodel = FILETYPE_MAP[self.filetype]
        q = self.db.query(dbmodel).filter_by(name=name)
        obj = q.one()
        content = self._get_object_content(obj)
        self._make_response(content)
        
        
    
                
