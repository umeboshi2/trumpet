from cStringIO import StringIO
from datetime import datetime

import transaction

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render
from pyramid.response import Response


from trumpet.models.sitecontent import SiteText

from trumpet.resources import MemoryTmpStore

from trumpet.managers.admin.images import ImageManager
from trumpet.managers.wiki import WikiArchiver


import colander
import deform

tmpstore = MemoryTmpStore()


class EditSiteTextSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        title='Name')
    content = colander.SchemaNode(
        colander.String(),
        title='Content',
        widget=deform.widget.TextAreaWidget(rows=10, cols=60))


    
