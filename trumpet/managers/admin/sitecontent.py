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

class SiteArchiver(object):
    def __init__(self, session):
        self.session = session

    def _serialize_path(self, path):
        return dict(id=path.id, name=path.name)

    def _serialize_sitecss(self, scss):
        path = scss.path.name
        css = scss.css.name
        return dict(path=path, css=css)

    def _serialize_sitejs(self, sjs):
        path = sjs.path.name
        js = sjs.js.name
        return dict(path=path, js=js)

    def archive_paths(self):
        for p in self.session.query(SitePath).all():
            pdict = self._serialize_path(p)
            self.pathcsv.writerow(pdict)
        pfilename = 'site-paths.csv'
        self.zipfile.writestr(pfilename, self.path_fileobj.getvalue())
        
    def archive_css_files(self):
        for c in self.session.query(SiteCSS).all():
            cfilename = 'css/%s.css' % c.name
            self.zipfile.writestr(cfilename, bytes(c.content))

    def archive_js_files(self):
        for j in self.session.query(SiteJS).all():
            jfilename = 'js/%s.js' % j.name
            self.zipfile.writestr(jfilename, bytes(j.content))

    def archive_template_files(self):
        for t in self.session.query(SiteTemplate).all():
            tfilename = 'templates/%s.txt' % t.name
            self.zipfile.writestr(tfilename, bytes(t.content))
            
    def archive_relations(self):
        for scss in self.session.query(SitePathCSS).all():
            sdict = self._serialize_sitecss(scss)
            self.csscsv.writerow(sdict)
        for sjs in self.session.query(SitePathJS).all():
            sdict = self._serialize_sitejs(sjs)
            self.jscsv.writerow(sdict)
        cfilename = 'site-path-css.csv'
        jfilename = 'site-path-js.csv'
        self.zipfile.writestr(cfilename, self.css_fileobj.getvalue())
        self.zipfile.writestr(jfilename, self.js_fileobj.getvalue())
        
    
    def create_new_zipfile(self):
        self.zipfileobj = BytesIO()
        self.zipfile = ZipFile(self.zipfileobj, 'w', ZIP_DEFLATED)
        path_fields = ['id', 'name']
        self.path_fileobj = StringIO()
        self.pathcsv = csv.DictWriter(self.path_fileobj, path_fields)
        css_fields = ['path', 'css']
        self.css_fileobj = StringIO()
        self.csscsv = csv.DictWriter(self.css_fileobj, css_fields)
        js_fields = ['path', 'js']
        self.js_fileobj = StringIO()
        self.jscsv = csv.DictWriter(self.js_fileobj, js_fields)

    def make_archive(self):
        self.create_new_zipfile()
        self.archive_paths()
        self.archive_css_files()
        self.archive_js_files()
        self.archive_template_files()
        self.archive_relations()
        self.zipfile.close()
        return self.zipfileobj.getvalue()
    
        
class SiteContentManager(object):
    def __init__(self, session):
        self.session = session

        # database objects
        self.dbcss = SiteCSS
        self.dbjs = SiteJS
        self.dbtemplate = SiteTemplate
        self.dbpath = SitePath
        
        # request object
        self.request = None

    def make_archive(self):
        archiver = SiteArchiver(self.session)
        return archiver.make_archive()

    def set_request(self, request):
        self.request = request
        
    def css_query(self):
        return self.session.query(self.dbcss)

    def js_query(self):
        return self.session.query(self.dbjs)

    def tmpl_query(self):
        return self.session.query(self.dbtemplate)

    def path_query(self):
        return self.session.query(self.dbpath)

    def ordered_path_list(self):
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

    def get_template_content(self, name):
        t = self.get_tmpl_by_name(name)
        return t.content
    
    def get_path_by_name(self, name):
        exc = NoContentFound
        q = self.session.query(SitePath)
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

    def add_css(self, name, content):
        return self._add(self.dbcss, name, content)

    def add_js(self, name, content):
        return self._add(self.dbjs, name, content)

    def add_template(self, name, content):
        return self._add(self.dbtemplate, name, content)

    def _update(self, name, content, byname):
        with transaction.manager:
            dbobj = byname(name)
            dbobj.content = content
        dbobj = self.session.merge(dbobj)
        return dbobj

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
        
    def update_template_by_name(self, name, content):
        byname = self.get_tmpl_by_name
        return self._update(name, content, byname)

    def update_template(self, template_id, content):
        with transaction.manager:
            t = self.session.query(SiteTemplate).get(template_id)
            t.content = content
        t = self.session.merge(t)
        return t
    
    
    def _add_sitepath(self, path, ret=False):
        with transaction.manager:
            sp = SitePath()
            sp.name = path
            self.session.add(sp)
        if ret:
            return self.session.merge(sp)

    def add_sitepath(self, path):
        return self._add_sitepath(path, ret=True)
    
    def update_sitepath(self, path):
        q = self.session.query(SitePath).filter_by(name=path)
        try:
            q.one()
        except NoResultFound:
            self._add_sitepath(path)
            
    
    def attach_css_to_path(self, path_id, css_id):
        with transaction.manager:
            dbobj = SitePathCSS()
            dbobj.path_id = path_id
            dbobj.css_id = css_id
            self.session.add(dbobj)
        return self.session.merge(dbobj)
    
    def attach_js_to_path(self, path_id, js_id):
        with transaction.manager:
            dbobj = SitePathJS()
            dbobj.path_id = path_id
            dbobj.js_id = js_id
            self.session.add(dbobj)
        return self.session.merge(dbobj)    

    def _get_dbobjs_for_path(self, path, dbobj):
        p = self.get_path_by_name(path)
        if p is not None:
            q = self.session.query(dbobj)
            q = q.filter_by(path_id=p.id)
            return q.all()
        else:
            return list()

    def _get_dbobjs_for_path_id(self, path_id, dbobj):
        q = self.session.query(dbobj)
        q = q.filter_by(path_id=path_id)
        return q.all()
    
    def get_css_for_path(self, path_id):
        return self._get_dbobjs_for_path_id(path_id, SitePathCSS)

    def get_js_for_path(self, path_id):
        return self._get_dbobjs_for_path_id(path_id, SitePathJS)
    
    def _css_tag(self, css_id):
        url = self.request.route_url('blob', filetype='css', id=css_id)
        tmpl = '<link rel="stylesheet" type="text/css" href="%s" />\n'
        return tmpl % url

    def _js_tag(self, js_id):
        url = self.request.route_url('blob', filetype='js', id=js_id)
        tmpl = '<script type="text/javascript" src="%s"></script>\n'
        return tmpl % url
    
    def get_css_tags(self, path_id):
        csslist = self._get_dbobjs_for_path_id(path_id, SitePathCSS)
        return (self._css_tag(css.css_id) for css in csslist)

    def get_js_tags(self, path_id):
        jslist = self._get_dbobjs_for_path_id(path_id, SitePathJS)
        return (self._js_tag(js.js_id) for js in jslist)

    
    def detach_css(self, path_id, css_id):
        with transaction.manager:
            s = self.session.query(SitePathCSS).get((path_id, css_id))
            self.session.delete(s)

    def detach_js(self, path_id, js_id):
        with transaction.manager:
            s = self.session.query(SitePathJS).get((path_id, js_id))
            self.session.delete(s)

    def delete_css(self, css_id):
        with transaction.manager:
            pcss = self.session.query(SitePathCSS).filter_by(css_id=css_id)
            if not pcss.count():
                css = self.css_query().get(css_id)
                self.session.delete(css)
            else:
                raise DeleteRestrictedError, "Unable to delete css"


            
    def delete_js(self, js_id):
        with transaction.manager:
            pjs = self.session.query(SitePathJS).filter_by(js_id=js_id)
            if not pjs.count():
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
        
        
        

    
