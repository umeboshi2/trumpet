import os
from zipfile import ZipFile, ZIP_DEFLATED
import csv
from io import BytesIO
from cStringIO import StringIO
from datetime import datetime

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import subqueryload

import transaction

from trumpet.models.sitecontent import SitePath
from trumpet.models.sitecontent import SiteTemplate
from trumpet.models.sitecontent import SiteCSS, SiteJS
from trumpet.models.sitecontent import SitePathCSS, SitePathJS

from trumpet.models.sitecontent import SiteWebview
from trumpet.models.sitecontent import SiteLayoutField
from trumpet.models.sitecontent import SiteLayoutModel
from trumpet.models.sitecontent import SiteLayoutModelField
from trumpet.models.sitecontent import SiteWebviewCSS
from trumpet.models.sitecontent import SiteWebviewJS



class NoContentFound(Exception):
    pass

class NoPathFound(Exception):
    pass

class NoTemplateFound(Exception):
    pass

class NoCSSFound(Exception):
    pass

class NoJSFound(Exception):
    pass

class DeleteRestrictedError(Exception):
    pass

        
class SiteWebviewManager(object):
    def __init__(self, session):
        self.session = session

        # database objects
        self.dbwebview = SiteWebview
        self.dbfield = SiteLayoutField
        self.dbmodel = SiteLayoutModel
        self.db_model_field = SiteLayoutModelField
        self.dbwebview_css = SiteWebviewCSS
        self.dbwebview_js = SiteWebviewJS

        self.dbtemplate = SiteTemplate
        self.dbcss = SiteCSS
        self.dbjs = SiteJS

        
        # request object
        self.request = None

    def set_request(self, request):
        self.request = request
        
    def tmpl_query(self):
        return self.session.query(self.dbtemplate)

    def css_query(self):
        return self.session.query(self.dbcss)

    def js_query(self):
        return self.session.query(self.dbjs)

    def field_query(self):
        return self.session.query(self.dbfield)
    
    def model_query(self):
        return self.session.query(self.dbmodel)

    def model_field_query(self):
        return self.session.query(self.db_model_field)

    def webview_query(self):
        return self.session.query(self.dbwebview)

    def ordered_webview_list(self):
        raise RuntimeError, "FIXME"
        q = self.path_query()
        q = q.options(joinedload(SitePath.css))
        q = q.options(joinedload(SitePath.js))
        q = q.order_by(SitePath.name)
        return q.all()
    
    
    def _get_by_name(self, name, query, not_there_exception):
        query = query.filter_by(name=name)
        try:
            return query.one()
        except NoResultFound:
            raise not_there_exception, "no object named %s" % name
        except OperationalError:
            raise not_there_exception, "no database?"

    def get_css_by_name(self, name):
        exc = NoCSSFound
        q = self.css_query()
        return self._get_by_name(name, q, exc)

    def get_js_by_name(self, name):
        exc = NoJSFound
        q = self.js_query()
        return self._get_by_name(name, q, exc)

    def get_tmpl_by_name(self, name):
        exc = NoTemplateFound
        q = self.tmpl_query()
        return self._get_by_name(name, q, exc)

    def get_webview_by_name(self, name):
        exc = NoContentFound
        q = self.session.query(SiteWebview)
        try:
            return self._get_by_name(name, q, exc)
        except exc:
            return None
        
    def _add(self, dbclass, name, content):
        with transaction.manager:
            dbobj = dbclass()
            dbobj.name = name
            dbobj.content = content
            self.session.add(dbobj)
        return self.session.merge(dbobj)

    def add_template(self, name, content):
        return self._add(self.dbtemplate, name, content)

    def add_css(self, name, content):
        return self._add(self.dbcss, name, content)

    def add_js(self, name, content):
        return self._add(self.dbjs, name, content)

    def _update(self, name, content, byname):
        with transaction.manager:
            dbobj = byname(name)
            dbobj.content = content
        dbobj = self.session.merge(dbobj)
        return dbobj

    def update_template_by_name(self, name, content):
        byname = self.get_tmpl_by_name
        return self._update(name, content, byname)

    def update_template(self, template_id, content):
        with transaction.manager:
            t = self.session.query(SiteTemplate).get(template_id)
            t.content = content
        t = self.session.merge(t)
        return t
    
    
    def update_css_by_name(self, name, content):
        byname = self.get_css_by_name
        return self._update(name, content, byname)

    def update_css(self, css_id, content):
        with transaction.manager:
            css = self.css_query().get(css_id)
            css.content = content
        css = self.session.merge(css)
        return css
    
    def update_js_by_name(self, name, content):
        byname = self.get_js_by_name
        return self._update(name, content, byname)

    def update_js(self, js_id, content):
        with transaction.manager:
            js = self.js_query().get(js_id)
            js.content = content
        js = self.session.merge(js)
        return js

    def list_fields(self):
        q = self.session.query(SiteLayoutField)
        return q.all()
    
    def add_field(self, name, type):
        with transaction.manager:
            f = SiteLayoutField()
            f.name = name
            f.type = type
            self.session.add(f)
        return self.session.merge(f)

    def list_models(self):
        return self.session.query(self.dbmodel).all()

    def add_model(self, name):
        with transaction.manager:
            m = SiteLayoutModel()
            m.name = name
            self.session.add(m)
        return self.session.merge(m)

    def attach_field_to_model(self, model_id, field_id, content):
        with transaction.manager:
            mf = self.db_model_field()
            mf.model_id = model_id
            mf.field_id = field_id
            mf.content = content
            self.session.add(mf)
        return self.session.merge(mf)

    def detach_field_from_model(self, model_id, field_id):
        with transaction.manager:
            mf = self.session.query(self.db_model_field).get((model_id, field_id))
            self.session.delete(mf)

    def update_field_on_model(self, model_id, field_id, content):
        with transaction.manager:
            mf = self.session.query(self.db_model_field).get((model_id, field_id))
            mf.content = content
            self.session.add(mf)
        return self.session.merge(mf)

    def add_webview(self, name, model_id, template_id, static_resources=None):
        with transaction.manager:
            w = self.dbwebview()
            w.name = name
            w.model_id = model_id
            w.template_id = template_id
            if static_resources is None:
                static_resources = []
            w.static_resources = static_resources
            self.session.add(w)
        return self.session.merge(w)

    def update_webview(self, id, name=None, model_id=None,
                       template_id=None, template=None,
                       static_resources=None):
        with transaction.manager:
            w = self.session.query(self.dbwebview).get(id)
            if w is None:
                raise NoContentFound, "unable to retrieve webview"
            update = False
            if name is not None:
                w.name = name
                update = True
            if model_id is not None:
                w.model_id = model_id
            if template_id is not None:
                w.template_id = template_id
                update = True
            if static_resources is not None:
                w.static_resources = static_resources
                update = True
            if template is not None:
                w.template.content = template
            if update:
                self.session.add(w)
        return self.session.merge(w)

            
    
    def attach_css_to_webview(self, path_id, css_id):
        with transaction.manager:
            dbobj = self.dbwebview_css()
            dbobj.path_id = path_id
            dbobj.css_id = css_id
            self.session.add(dbobj)
        return self.session.merge(dbobj)
    
    def attach_js_to_webview(self, path_id, js_id):
        with transaction.manager:
            dbobj = self.dbwebview_js()
            dbobj.path_id = path_id
            dbobj.js_id = js_id
            self.session.add(dbobj)
        return self.session.merge(dbobj)    

    def _get_dbobjs_for_webview(self, webview_id, dbobj):
        q = self.session.query(dbobj)
        q = q.filter_by(path_id=webview_id)
        return q.all()

    def get_css_for_webview(self, path_id):
        return self._get_dbobjs_for_webview(path_id, SiteWebviewCSS)

    def get_js_for_webview(self, path_id):
        return self._get_dbobjs_for_webview(path_id, SiteWebviewJS)

    def _css_tag(self, css_id):
        url = self.request.route_url('blob', filetype='css', id=css_id)
        tmpl = '<link rel="stylesheet" type="text/css" href="%s" />\n'
        return tmpl % url

    def _js_tag(self, js_id):
        url = self.request.route_url('blob', filetype='js', id=js_id)
        tmpl = '<script type="text/coffeescript" src="%s"></script>\n'
        return tmpl % url
    
    def get_css_tags(self, path_id):
        csslist = self.get_css_for_webview(path_id)
        return (self._css_tag(css.css_id) for css in csslist)

    def get_js_tags(self, path_id):
        jslist = self.get_js_for_webview(path_id)
        return (self._js_tag(js.js_id) for js in jslist)

    
    def detach_css(self, path_id, css_id):
        with transaction.manager:
            s = self.session.query(SiteWebviewCSS).get((path_id, css_id))
            self.session.delete(s)

    def detach_js(self, path_id, js_id):
        with transaction.manager:
            s = self.session.query(SiteWebviewJS).get((path_id, js_id))
            self.session.delete(s)

    def delete_css(self, css_id):
        with transaction.manager:
            total = 0
            pcss = self.session.query(SitePathCSS).filter_by(css_id=css_id)
            total += pcss.count()
            wcss = self.session.query(SiteWebviewCSS).filter_by(css_id=css_id)
            total += pcss.count()
            if not total:
                css = self.css_query().get(css_id)
                self.session.delete(css)
            else:
                raise DeleteRestrictedError, "Unable to delete css"


            
    def delete_js(self, js_id):
        with transaction.manager:
            total = 0
            pjs = self.session.query(SitePathJS).filter_by(js_id=js_id)
            total += pjs.count()
            wjs = self.session.query(SiteWebviewJS).filter_by(js_id=js_id)
            total += pjs.count()
            if not total:
                js = self.js_query().get(js_id)
                self.session.delete(js)
            else:
                raise DeleteRestrictedError, "Unable to delete js"


            
class SiteArchiveImporter(object):
    def __init__(self, session):
        self.session = session
        self.mgr = SiteContentManager(self.session)
        self.zipfile = None
        
        # database objects
        self.dbcss = SiteCSS
        self.dbjs = SiteJS
        self.dbtemplate = SiteTemplate
        self.dbpath = SitePath

    def set_zipfile(self, zipstream):
        self.zipfileobj = BytesIO(zipstream)
        # is this seek necessary?
        self.zipfileobj.seek(0)
        self.zipfile = ZipFile(self.zipfileobj, 'r')

    def clear_database(self):
        with transaction.manager:
            for o in [SitePathCSS, SitePathJS, SiteCSS,
                      SiteJS, SiteTemplate, SitePath]:
                q = self.session.query(o)
                q.delete()

    def import_site_paths(self):
        filename = 'site-paths.csv'
        content = self.zipfile.read(filename)
        pfile = StringIO(content)
        reader = csv.reader(pfile)
        for id, path in reader:
            self.mgr.update_sitepath(path)

    def _import_resources(self, prefix, suffix, add_method):
        namelist = self.zipfile.namelist()
        files = [n for n in namelist if n.startswith(prefix)]
        for pathname in files:
            print "PathName", pathname
            filename = os.path.basename(pathname)
            print "FileName", filename
            if not pathname.endswith(suffix):
                raise RuntimeError, "Unexpected file %s" % pathname
            name = filename[:-len(suffix)]
            print "NAME:", name
            content = self.zipfile.read(pathname)
            add_method(name, content)
            
    def import_css(self):
        self._import_resources('css/', '.css', self.mgr.add_css)

    def import_js(self):
        self._import_resources('js/', '.js', self.mgr.add_js)


    def _site_path_reader(self, filename):
        content = self.zipfile.read(filename)
        pfile = StringIO(content)
        return csv.reader(pfile)
    
    def import_site_path_relations(self):
        cssreader = self._site_path_reader('site-path-css.csv')
        for spath, name in cssreader:
            path = self.mgr.get_path_by_name(spath)
            if path is None:
                raise RuntimeError, "Path %s not found" % spath
            path_id = path.id
            css = self.mgr.get_css_by_name(name)
            css_id = css.id
            self.mgr.attach_css_to_path(path_id, css_id)
        jsreader = self._site_path_reader('site-path-js.csv')
        for spath, name in jsreader:
            path = self.mgr.get_path_by_name(spath)
            if path is None:
                raise RuntimeError, "Path %s not found" % spath
            path_id = path.id
            js = self.mgr.get_js_by_name(name)
            js_id = js.id
            self.mgr.attach_js_to_path(path_id, js_id)
        
    def import_site_archive(self):
        if self.zipfile is None:
            raise RuntimeError, "Set zipfile first."
        self.clear_database()
        self.import_css()
        self.import_js()
        self.import_site_paths()
        self.import_site_path_relations()
        
        
        

    
