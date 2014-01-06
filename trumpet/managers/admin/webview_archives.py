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

    def archive_layout_fields(self):
        for f in self.session.query(SiteLayoutField).all():
            df = f.serialize()
            self.lfieldcsv.writerow(df)
        filename = 'layout-fields.csv'
        self.zipfile.writestr(filename, self.layout_field_fileobj.getvalue())
        
    def archive_layout_models(self):
        pass
    
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
        # layout fields
        layout_field_fields = ['id', 'name', 'type']
        self.layout_field_fileobj = StringIO()
        self.lfieldcsv = csv.DictWriter(self.layout_field_fileobj,
                                        layout_field_fields)
        # layout models
        layout_model_fields = ['id', 'name']
        self.layout_model_fileobj = StringIO()
        self.lmodelcsv = csv.DictWriter(self.layout_model_fileobj,
                                        layout_model_fields)
        # layout model fields
        lmfield_fields = ['field_id', 'model_id', 'content']
        self.layout_model_fields_fileobj = StringIO()
        self.lmfcsv = csv.DictWriter(self.layout_model_fields_fileobj,
                                     lmfield_fields)
        css_fields = ['path', 'css']
        self.css_fileobj = StringIO()
        self.csscsv = csv.DictWriter(self.css_fileobj, css_fields)
        js_fields = ['path', 'js']
        self.js_fileobj = StringIO()
        self.jscsv = csv.DictWriter(self.js_fileobj, js_fields)

    def make_archive(self):
        self.create_new_zipfile()
        #self.archive_paths()
        self.archive_css_files()
        self.archive_js_files()
        self.archive_template_files()
        self.archive_relations()
        self.zipfile.close()
        return self.zipfileobj.getvalue()
    
        
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
        
        
        

    
