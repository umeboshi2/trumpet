import os
from datetime import datetime

import transaction
from docutils.core import publish_parts
from formencode.htmlgen import html

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



from menus import BaseMenu, TopBar


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


def make_main_menu(request):
    menu = BaseMenu(header='Main Menu', class_='submenu')
    user = request.session.get('user', None)
    logged_in = user is not None
    if 'user' in request.session:
        user = request.session['user']
        url = request.route_url('view_wiki')
        menu.append_new_entry('Wiki', url)
        
        url = request.route_url('consult_contacts', context='list', id='all')
        menu.append_new_entry('Contacts', url)

        url = request.route_url('consult_clients', context='list', id='all')
        menu.append_new_entry('Clients', url)

        url = request.route_url('consult_calendar', context='list', id='all')
        menu.append_new_entry('Calendar', url)

        url = request.route_url('consult_tickets', context='main', id='all')
        menu.append_new_entry('Tickets', url)

    return menu
    

def prepare_layout(layout):
    layout.title = 'Base Page'
    layout.header = layout.title
    
class BaseViewer(object):
    def __init__(self, request):
        self.request = request
        self.layout = self.request.layout_manager.layout
        prepare_layout(self.layout)
        self.layout.main_menu = make_main_menu(self.request)
        self.response = None
        self.content_mgr = SiteContentManager(self.request.db)
        self.content_mgr.set_request(self.request)
        self._update_sitepath()
        self._generate_layout_resources()
        # empty dispatch table
        if hasattr(self, '_dispatch_table'):
            self.dispatch()

    def _update_sitepath(self):
        rpath = self.request.path
        md = self.request.matchdict
        keys = md.keys()
        keys.sort()
        if keys == ['context', 'id']:
            dirname, basename = os.path.split(rpath)
            if md['id'] == basename:
                rpath = dirname
            try:
                self.content_mgr.update_sitepath(rpath)
            except OperationalError:
                try:
                    self.content_mgr.dbpath.metadata.create_all()
                except UnboundExecutionError:
                    pass
        self.current_path = rpath

    def _generate_layout_resources(self):
        pass
    

    def dispatch(self):
        view = self._view
        if view in self._dispatch_table:
            self._dispatch_table[view]()
        else:
            msg = 'Undefined View: %s' % view
            self.layout.content = '<b>%s</b>' % msg
            
        
    def __call__(self):
        if self.response is not None:
            return self.response
        else:
            return {}

    def url(self, route=None, **kw):
        if route is None:
            route = self.request.matched_route.name
        url = self.request.route_url(route, **kw)
        return url

    def link(self, value, **kw):
        url = self.url(**kw)
        return html.a(value, href=url)

    def make_menu(self, header, entries, class_='submenu'):
        menu = BaseMenu(header=header, class_=class_)
        for value, href in entries:
            menu.append_new_entry(value, href)
        return menu

    def render(self, template, env):
        if 'view' not in env:
            env['view'] = self
        return render(template, env, request=self.request)

    def _render_template(self, template, env):
        t = Template(template)
        if 'view' not in env:
            env['view'] = self
        if 'request' not in env:
            env['request'] = self.request
        try:
            content = t.render(**env)
        except NameError:
            return "Undefined name in template"
        except TypeError:
            return "Unknown error in template"
        except SyntaxException:
            return "Syntax exception encountered in template"
        except SyntaxError:
            return "Syntax error encountered in template"
        except MakoException:
            return "Encountered MakoException"
        return content
    
    def dbrender(self, name, env):
        try:
            template = self.content_mgr.get_template_content(name)
        except NoTemplateFound, e:
            return str(e)
        return self._render_template(template, env)
    
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
    

class AdminViewer(BaseViewer):
    def __init__(self, request):
        super(AdminViewer, self).__init__(request)


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
    
