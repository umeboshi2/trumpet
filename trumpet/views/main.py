from datetime import datetime

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid


from base import prepare_layout
from base import BaseViewer
from menus import BaseMenu


def prepare_main_data(request):
    layout = request.layout_manager.layout
    layout.title = 'Main Page'
    layout.header = 'Main Page'
    menu = BaseMenu()
    menu.set_header('Main Menu')
    if 'user' not in request.session:
        url = request.route_url('login')
        menu.append_new_entry('login', url)
    else:
        user = request.session['user']
        if user.username == 'admin':
            url = request.route_url('admin')
            menu.append_new_entry('Administer Site', url)
            url = request.route_url('rssviewer', context='listfeeds', feed=None)
            menu.append_new_entry('rss', url)
    url = request.route_url('view_wiki')
    menu.append_new_entry('wiki', url)
    url = request.route_url('consult')
    menu.append_new_entry('Consultant', url)
    layout.main_menu = menu
    

class MainViewer(BaseViewer):
    def __init__(self, request):
        super(MainViewer, self).__init__(request)
        prepare_main_data(self.request)
        #self.layout.resources.bootstrap.bootstrap_js.need()
        
