from cStringIO import StringIO
from datetime import datetime
import json

import transaction

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render
from pyramid.response import Response

from trumpet.managers.admin.sitewebview import SiteWebviewManager


from trumpet.models.sitecontent import SiteText
from trumpet.managers.admin.sitecontent import SiteArchiveImporter
from trumpet.managers.admin.sitecontent import DeleteRestrictedError

from trumpet.resources import MemoryTmpStore

from trumpet.views.base import BasicView

from trumpet.views.schema import NameSelectSchema, UploadFileSchema
from trumpet.views.schema import make_select_widget, deferred_choices


import colander
import deform

tmpstore = MemoryTmpStore()

class TextSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        title='Name')
    content = colander.SchemaNode(
        colander.String(),
        title='Content',
        widget=deform.widget.TextAreaWidget(rows=10, cols=60))

fieldtypes = (
    ('text', 'text'),
    ('html', 'html'),
    ('teacup', 'teacup'),
    )

class FieldSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        title='Name')
    type = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.SelectWidget(values=fieldtypes),
        title='type')


class ModelSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        title='Name')


class WebViewSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        title='Name')
    model_id = colander.SchemaNode(
        colander.Integer(),
        title='Model',
        widget=deferred_choices,)
    template_id = colander.SchemaNode(
        colander.Integer(),
        title='Template',
        widget=deferred_choices,)
    
class CSSSchema(colander.Schema):
    css_id = colander.SchemaNode(
        colander.Integer(),
        title='CSS',
        widget=deferred_choices,)

class JSSchema(colander.Schema):
    js_id = colander.SchemaNode(
        colander.Integer(),
        title='JS',
        widget=deferred_choices,)
    
    
class MainViewer(BasicView):
    def __init__(self, request):
        super(MainViewer, self).__init__(request)
        self.mgr = SiteWebviewManager(self.request.db)
        
        self._dispatch_table = dict(
            mkarchive=self.make_archive,
            importarchive=self.import_archive,
            )

        
        self.context = self.request.matchdict['context']
        self._view = self.context

        self.dispatch()

    ###################################################
    # FIXME: update archive methods
    ###################################################
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
    

