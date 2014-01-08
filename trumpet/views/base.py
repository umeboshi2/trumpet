import os
from datetime import datetime

import transaction
from docutils.core import publish_parts

from mako.template import Template
from mako.exceptions import MakoException
from mako.exceptions import SyntaxException

from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.orm.exc import NoResultFound

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render
from pyramid.response import FileResponse
from pyramid.path import AssetResolver



from trumpet.models.base import DBSession
from trumpet.models.usergroup import User

from trumpet.managers.admin.sitecontent import SiteContentManager
from trumpet.managers.admin.sitecontent import NoTemplateFound


def static_asset_response(request, asset):
    resolver = AssetResolver()
    descriptor = resolver.resolve(asset)
    if not descriptor.exists():
        raise HTTPNotFound(request.url)
    path = descriptor.abspath()
    response = FileResponse(path, request)
    zip_response = False
    for ending in ['.css', '.js', '.coffee', '.html', '.ttf']:
        if path.endswith(ending):
            zip_response = True
    if zip_response:
        response.encode_content()
    return response




def render_rst(content):
    return publish_parts(content, writer_name='html')['html_body']


class BasicView(object):
    def __init__(self, request):
        self.request = request
        self.response = None
        self.data = {}
    
    def __call__(self):
        if self.response is not None:
            return self.response
        else:
            return self.data

    def get_current_user_id(self):
        "Get the user id quickly without db query"
        return self.request.session['user'].id

    def get_current_user(self):
        "Get user db object"
        db = self.request.db
        user_id = self.request.session['user'].id
        return db.query(User).get(user_id)

    def get_app_settings(self):
        return self.request.registry.settings

STATIC_VIEWS = ['lib', 'css', 'components', 'fonts']
class StaticView(BasicView):
    def __init__(self, request):
        super(StaticView, self).__init__(request)
        view = request.view_name
        if view in STATIC_VIEWS:
            path = os.path.join('static', view, *request.subpath)
            asset = ':'.join(('trumpet', path))
            self.response = static_asset_response(request, asset)
        else:
            raise HTTPNotFound()
        
        
