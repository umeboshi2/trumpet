from cStringIO import StringIO
from datetime import datetime

import transaction
from PIL import Image

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render

from trumpet.models.base import DBSession
from trumpet.models.sitecontent import SiteImage

from trumpet.views.menus import BaseMenu


from trumpet.views.base import AdminViewer

def make_main_menuNew(request):
    menu = BaseMenu()
    menu.set_header('Admin Menu')
    #url = request.route_url('admin_users', context='list', id='all')
    url = request.route_url('admin', traverse='users')
    menu.append_new_entry('Manage Users', url)
    url = request.route_url('admin', resource='sitetext', context='list',
                            traverse=[])
    menu.append_new_entry('Manage Text', url)
    url = request.route_url('admin', resource='images', context='list',
                            traverse=[])
    menu.append_new_entry('Manage Images', url)
    url = request.route_url('admin', resource='dbadmin', context='main',
                            traverse=[])
    menu.append_new_entry('Manage Database', url)
    
    url = request.route_url('admin', resource='site_templates',
                            context='list', traverse=[])
    menu.append_new_entry('Site Templates', url)

    url = request.route_url('admin', resource='sitecontent_mgr',
                            context='listpaths', traverse=[])
    menu.append_new_entry('Site Content', url)
    return menu


def make_main_menuOrig(request):
    menu = BaseMenu()
    menu.set_header('Admin Menu')

    url = request.route_url('admin_webviews', context='listwebviews',
                            id='all')
    menu.append_new_entry('webviews', url)
    
    
    url = request.route_url('admin_users', context='list', id='all')
    menu.append_new_entry('Manage Users', url)
    #url = request.route_url('admin_users_bb')
    #menu.append_new_entry('Manage Users bb', url)
    url = request.route_url('admin_sitetext', context='list', id=None)
    menu.append_new_entry('Manage Text', url)
    url = request.route_url('admin_images', context='list', id=None)
    menu.append_new_entry('Manage Images', url)
    #url = request.route_url('admin_site_templates',
    #                        context='list', id='all')
    #menu.append_new_entry('Site Templates', url)
    url = request.route_url('admin_sitecontent_mgr',
                            context='listpaths', id='all')
    menu.append_new_entry('Site Content', url)
    url = request.route_url('admin_sitecontent_mgr_bb',
                            context='listpaths', id='all')
    menu.append_new_entry('Site Content(backbone)', url)
    return menu


make_main_menu = make_main_menuOrig

class MainViewer(AdminViewer):
    def __init__(self, request):
        super(MainViewer, self).__init__(request)
        self.layout.main_menu = make_main_menu(self.request)
        

