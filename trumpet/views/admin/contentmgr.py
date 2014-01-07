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


from trumpet.views.schema import NameSelectSchema, UploadFileSchema
from trumpet.views.schema import make_select_widget

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


    
