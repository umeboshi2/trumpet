from cStringIO import StringIO
from datetime import datetime

import transaction
from PIL import Image

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.renderers import render

from trumpet.models.base import DBSession
from trumpet.models.sitecontent import SiteImage

from trumpet.views.menus import BaseMenu

import colander
import deform


from trumpet.views.base import AdminViewer
from trumpet.views.admin.base import make_main_menu

from trumpet.resources import Resource



def prepare_main_data(request):
    layout = request.layout_manager.layout

    layout.title = 'Admin Page'
    layout.header = 'Admin Page'
    menu = make_main_menu(request)
    #layout.options_menus = dict(admin=menu)
    layout.main_menu = menu
    

class AdminRoot(Resource):
    __acl__ = [
        (Allow, 'admin', 'admin'),
        ]

    def __init__(self, request):
        for key in ['users', 'images', 'sitetext',
                    'dbadmin', 'site_templates',
                    'sitecontent_mgr']:
            self[key] = Resource(key, self)
            

    
def admin_root_factory(request):
    return AdminRoot(request)

        
    
    
    
class MainViewer(AdminViewer):
    def __init__(self, request):
        super(MainViewer, self).__init__(request)
        prepare_main_data(request)
