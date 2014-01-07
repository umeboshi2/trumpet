from cStringIO import StringIO
from datetime import datetime

import transaction

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.renderers import render


from trumpet.resources import MemoryTmpStore


from trumpet.managers.admin.images import ImageManager

import colander
import deform

tmpstore = MemoryTmpStore()


class AddImageSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        title = 'Image Name',
        )
    upload = colander.SchemaNode(
        deform.FileData(),
        widget=deform.widget.FileUploadWidget(tmpstore)
        )
    
    
