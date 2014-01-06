from cStringIO import StringIO
from datetime import datetime
import json

import transaction

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render
from pyramid.response import Response


from trumpet.models.sitecontent import SiteText
from trumpet.managers.admin.sitecontent import SiteArchiveImporter
from trumpet.managers.admin.sitecontent import DeleteRestrictedError

from trumpet.resources import MemoryTmpStore

from trumpet.views.menus import BaseMenu
from trumpet.views.schema import NameSelectSchema, UploadFileSchema
from trumpet.views.schema import make_select_widget

from trumpet.views.base import BaseViewer as AdminViewer
from trumpet.views.admin.base import make_main_menu

import colander
import deform

tmpstore = MemoryTmpStore()

def prepare_main_data(request):
    layout = request.layout_manager.layout
    layout.main_menu = make_main_menu(request)
    
    menu = BaseMenu()
    route = 'admin_sitecontent_mgr'
    mkurl = request.route_url

    url = mkurl(route, context='listpaths', id='all')
    menu.append_new_entry('List Paths', url)
    url = mkurl(route, context='listcss', id='all')
    menu.append_new_entry('List CSS', url)
    url = mkurl(route, context='listjs', id='all')
    menu.append_new_entry('List JS', url)
    menu.set_header('Actions')
    layout.options_menus = dict(actions=menu)
    
    title = 'Manage Site Content'
    layout.title = title
    layout.header = title
    
class TextSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        title='Name')
    content = colander.SchemaNode(
        colander.String(),
        title='Content',
        widget=deform.widget.TextAreaWidget(rows=10, cols=60))


    
class AppViewer(AdminViewer):
    def __init__(self, request):
        super(AppViewer, self).__init__(request)
        self.layout.resources.admin_content_manager.need()
        self.layout.main_menu = make_main_menu(self.request)
        self._set_menu()
        self.layout.sidebar = ''
        self.layout.content = '<div class="right-listview"></div>'
        ace = self.layout.resources.ace
        #self.layout.resources.admin_edit_site_resources.need()
        ace.worker_css.need()
        ace.worker_javascript.need()
        ace.mode_css.need()
        ace.mode_javascript.need()
        ace.mode_ejs.need()
        ace.theme_twilight.need()
        ace.theme_cobalt.need()
        ace.worker_coffee.need()
        ace.mode_coffee.need()
        self.layout.resources.jqueryui.need()
        self.layout.resources.ace_theme_trumpet.need()
        
    def _set_menu(self):
        menu = BaseMenu()
        menu.set_header("Actions")

        mkurl = self.url
        
        url = mkurl(context='listpaths', id='all')
        menu.append_new_entry('List Paths', url)
        url = mkurl(context='listcss', id='all')
        menu.append_new_entry('List CSS', url)
        url = mkurl(context='addcss', id='new')
        menu.append_new_entry('Add New CSS', url)
        url = mkurl(context='listjs', id='all')
        menu.append_new_entry('List JS', url)
        url = mkurl(context='addjs', id='new')
        menu.append_new_entry('Add New JS', url)
        url = mkurl(context='mkarchive', id='all')
        menu.append_new_entry('Site Archive', url)
        url = mkurl(context='importarchive', id='new')
        menu.append_new_entry('Import Archive', url)
        self.layout.options_menus = dict(actions=menu)

class MainViewer(AdminViewer):
    def __init__(self, request):
        super(MainViewer, self).__init__(request)
        #self.layout.subheader = self.request.method
        
        self._dispatch_table = dict(
            listpaths=self.list_paths,
            listcss=self.list_resources,
            addcss=self.add_css,
            listjs=self.list_resources,
            addjs=self.add_js,
            attachcss=self.attach_css,
            attachjs=self.attach_js,
            showcontent=self.show_path_content,
            showcss=self.show_css,
            showjs=self.show_js,
            detach=self.detach_file,
            mkarchive=self.make_archive,
            importarchive=self.import_archive,
            )
        self.context = self.request.matchdict['context']
        self._view = self.context

        
        self.dispatch()

    def _set_menu(self):
        menu = BaseMenu()
        menu.set_header("Actions")
        route = 'admin_sitecontent_mgr_bb'
        mkurl = self.request.route_url
        
        url = mkurl(route, context='listpaths', id='all')
        menu.append_new_entry('List Paths', url)
        url = mkurl(route, context='listcss', id='all')
        menu.append_new_entry('List CSS', url)
        url = mkurl(route, context='addcss', id='new')
        menu.append_new_entry('Add New CSS', url)
        url = mkurl(route, context='listjs', id='all')
        menu.append_new_entry('List JS', url)
        url = mkurl(route, context='addjs', id='new')
        menu.append_new_entry('Add New JS', url)
        url = mkurl(route, context='mkarchive', id='all')
        menu.append_new_entry('Site Archive', url)
        url = mkurl(route, context='importarchive', id='new')
        menu.append_new_entry('Import Archive', url)
        self.layout.options_menus = dict(actions=menu)
        
        

            
    def list_paths(self):
        template = 'trumpet:templates/admin-list-site-paths.mako'
        paths = self.content_mgr.ordered_path_list()
        env = dict(paths=paths)
        self.layout.content = self.render(template, env)

    def _update_resource(self):
        data = dict()
        if 'update' in self.request.POST:
            data = dict(self.request.POST)
            if data['update'] == 'delete':
                ctype = data['ctype']
                id = int(data['id'])
                if ctype == 'css':
                    q = self.content_mgr.css_query()
                    delete = self.content_mgr.delete_css
                elif ctype == 'js':
                    q = self.content_mgr.js_query()
                    delete = self.content_mgr.delete_js
                else:
                    raise RuntimeError, "Bad ctype %s" % ctype
                try:
                    delete(id)
                    data['update'] = 'deleted'
                except DeleteRestrictedError:
                    data['update'] = 'restricted'
        self.response = Response(json.dumps(data))

    def list_resources(self):
        if self.request.method == 'POST':
            self._update_resource()
            return
        if self.context == 'listcss':
            ctype = 'css'
            rlist = self.content_mgr.css_query().all()
        elif self.context == 'listjs':
            ctype = 'js'
            rlist = self.content_mgr.js_query().all()
        template = 'trumpet:templates/admin-list-site-resources.mako'
        env = dict(ctype=ctype, rlist=rlist)
        self.layout.content = self.render(template, env)
        self.layout.resources.admin_list_site_resources.need()
        

    def _text_form(self):
        schema = TextSchema()
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        return form
    
    def _add_content_submitted(self, form, ctype):
        controls = self.request.POST.items()
        self.layout.subheader = "submitted to database"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        name = data['name']
        content = data['content']
        if ctype == 'css':
            self.content_mgr.add_css(name, content)
        elif ctype == 'js':
            self.content_mgr.add_js(name, content)

    def _add_content(self, ctype):
        form = self._text_form()
        if 'submit' in self.request.POST:
            self._add_content_submitted(form, ctype)
        else:
            self.layout.content = form.render()
        
    def add_css(self):
        self._add_content('css')
        
    def add_js(self):
        self._add_content('js')
        
    def show_path_content(self):
        self.layout.resources.admin_show_path_content.need()
        path_id = int(self.request.matchdict['id'])
        path = self.content_mgr.path_query().get(path_id)
        csslist = self.content_mgr.get_css_for_path(path_id)
        jslist = self.content_mgr.get_js_for_path(path_id)
        env = dict(csslist=csslist, jslist=jslist, path=path)
        template = 'trumpet:templates/admin-show-site-path-content.mako'
        self.layout.content = self.render(template, env)

    def _edit_content_submitted(self, ctype):
        data = self.request.POST
        content = data['content']
        id = int(self.request.matchdict['id'])
        if ctype == 'css':
            self.content_mgr.update_css(id, content)
        elif ctype == 'js':
            self.content_mgr.update_js(id, content)
        url = self.url(context='show%s' % ctype, id=id)
        self.response = HTTPFound(url)
    
    def show_css(self):
        css_id = int(self.request.matchdict['id'])
        css = self.content_mgr.css_query().get(css_id)
        #data = dict(name=css.name, content=css.content)
        if 'update' in self.request.POST:
            self._edit_content_submitted('css')
        else:
            ace = self.layout.resources.ace
            self.layout.resources.admin_edit_site_resources.need()
            ace.worker_css.need()
            ace.mode_css.need()
            ace.theme_twilight.need()
            ace.theme_cobalt.need()
            template = 'trumpet:templates/admin-edit-sitecontent.mako'
            env = dict(content=css.content, name=css.name, ctype='css')
            self.layout.content = self.render(template, env)
        
    def show_js(self):
        js_id = int(self.request.matchdict['id'])
        js = self.content_mgr.js_query().get(js_id)
        if 'update' in self.request.POST:
            self._edit_content_submitted('js')
        else:
            ace = self.layout.resources.ace
            self.layout.resources.admin_edit_site_resources.need()
            ace.worker_javascript.need()
            ace.mode_javascript.need()
            ace.theme_twilight.need()
            ace.theme_cobalt.need()
            template = 'trumpet:templates/admin-edit-sitecontent.mako'
            env = dict(content=js.content, name=js.name, ctype='js')
            self.layout.content = self.render(template, env)
        

    def _nameselect_form(self, olist):
        schema = NameSelectSchema()
        choices = ((o.id, o.name) for o in olist)
        schema['name'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        return schema, form

    def _attach_form_submitted(self, form, ctype):
        controls = self.request.POST.items()
        self.layout.subheader = "submitted to database"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        path_id = int(self.request.matchdict['id'])
        cid = data['name']
        if ctype == 'css':
            self.content_mgr.attach_css_to_path(path_id, cid)
        elif ctype == 'js':
            self.content_mgr.attach_js_to_path(path_id, cid)
        url = self.url(context='showcontent', id=path_id)
        self.response = HTTPFound(url)

    def _attach_to_path(self, ctype):
        path_id = int(self.request.matchdict['id'])
        path = self.content_mgr.path_query().get(path_id)
        if ctype == 'css':
            olist = self.content_mgr.css_query().all()
        elif ctype == 'js':
            olist = self.content_mgr.js_query().all()
        else:
            raise RuntimeError, "Bad type %s" % ctype
        schema, form = self._nameselect_form(olist)
        if 'submit' in self.request.POST:
            self._attach_form_submitted(form, ctype)
        else:
            self.layout.content = form.render()
        
    def attach_css(self):
        self._attach_to_path('css')
        
    def attach_js(self):
        self._attach_to_path('js')

    def detach_file(self):
        id = self.request.matchdict['id']
        ctype, p, o = id.split('-')
        p = int(p)
        o = int(o)
        if ctype == 'css':
            self.content_mgr.detach_css(p, o)
        elif ctype == 'js':
            self.content_mgr.detach_js(p, o)
        url = self.url(context='showcontent', id=p)
        self.response = HTTPFound(url)
        
           
    def make_archive(self):
        archive = self.content_mgr.make_archive()
        content_type = 'application/zip'
        r = Response(content_type=content_type, body=archive)
        r.content_disposition = 'attachment; filename="site-archive.zip"'
        self.response = r
        
    def _site_archive_file_submitted(self, form):
        upload = self.request.POST['upload']
        if not hasattr(upload, 'filename'):
            self.layout.content = 'try again'
            return
        fname = upload.filename
        content = upload.file.read()
        importer = SiteArchiveImporter(self.request.db)
        importer.set_zipfile(content)
        importer.import_site_archive()
        self.layout.content = "Site Imported."
        
    
    def import_archive(self):
        schema = UploadFileSchema()
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            self._site_archive_file_submitted(form)
        else:
            self.layout.content = form.render()
    

