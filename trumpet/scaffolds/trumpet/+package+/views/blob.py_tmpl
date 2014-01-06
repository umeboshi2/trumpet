from datetime import datetime

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound


from trumpet.models.sitecontent import SiteImage
from trumpet.models.sitecontent import SiteCSS, SiteJS


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
            js=self.get_js,)

        # dispatch filetype request
        if self.filetype in self._viewmap:
            self._viewmap[self.filetype]()
        else:
            self.content = HTTPNotFound()
            
    def __call__(self):
        return self.content

    def get_image(self):
        id = self.request.matchdict['id']
        i = self.db.query(SiteImage).get(id)

        content = i.content
        # FIXME
        content_type = 'image/png'
        response = Response(body=i.content,
                            content_type=content_type)
        self.content = response
    
    def get_thumb(self):
        id = self.request.matchdict['id']
        i = self.db.query(SiteImage).get(id)
        # FIXME
        content_type = 'image/jpeg'
        response = Response(body=i.thumbnail,
                            content_type=content_type)
        self.content = response
    
    def get_css(self):
        id = self.request.matchdict['id']
        i = self.db.query(SiteCSS).get(id)
        # FIXME
        content_type = 'text/css'
        response = Response(body=i.content,
                            content_type=content_type)
        self.content = response

    
    def get_js(self):
        id = self.request.matchdict['id']
        i = self.db.query(SiteJS).get(id)
        # FIXME
        content_type = 'text/javascript'
        response = Response(body=i.content,
                            content_type=content_type)
        self.content = response

    
                
