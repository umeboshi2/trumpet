from datetime import datetime

import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import PickleType
from sqlalchemy import Enum


from sqlalchemy.orm import relationship, backref

from base import Base
from base import SerialBase

from base import DBSession
from sqlalchemy.exc import IntegrityError

class SiteImage(Base, SerialBase):
    __tablename__ = 'site_images'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), unique=True)
    content = Column(PickleType)
    thumbnail = Column(PickleType)
    
    def __init__(self, name=None, content=None):
        self.name = name
        self.content = content
        
    def __repr__(self):
        return self.name

    def serialize2(self):
        data = dict(id=self.id, name=self.name,
                    content=self.content, thumbnail=self.thumbnail)
        return data
    
    
        
VALID_TEXT_TYPES = ['html',
                    'rst', # restructured text
                    'md', # markdown
                    'tutwiki', # restructured text wiki tutorial
                    'text',] # just plain text

SiteTextType = Enum(*VALID_TEXT_TYPES, name='site_text_type')

class SitePath(Base, SerialBase):
    __tablename__ = 'site_view_paths'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(500), unique=True)
    
class SiteText(Base, SerialBase):
    __tablename__ = 'site_text'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), unique=True)
    type = Column(Unicode(25))
    content = Column(UnicodeText)
    created = Column(DateTime)
    modified = Column(DateTime)
    
    def __init__(self, name=None, content=None, type='html'):
        self.name = name
        self.type = type
        self.content = content
        self.created = datetime.now()
        self.modified = datetime.now()

        
class SiteTemplate(Base, SerialBase):
    __tablename__ = 'site_templates'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    content = Column(UnicodeText)
    description = Column(UnicodeText)
    created = Column(DateTime)
    modified = Column(DateTime)
    
    def __init__(self, name=None, content=None):
        self.name = name
        self.content = content
        self.created = datetime.now()
        self.modified = datetime.now()

class SiteCSS(Base, SerialBase):
    __tablename__ = 'site_css_resources'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    content = Column(UnicodeText)
    description = Column(UnicodeText)
    created = Column(DateTime)
    modified = Column(DateTime)

    def __init__(self, name=None, content=None):
        self.name = name
        self.content = content
        self.created = datetime.now()
        self.modified = datetime.now()

class SiteJS(Base, SerialBase):
    __tablename__ = 'site_js_resources'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    content = Column(UnicodeText)
    description = Column(UnicodeText)
    created = Column(DateTime)
    modified = Column(DateTime)
    
    def __init__(self, name=None, content=None):
        self.name = name
        self.content = content
        self.created = datetime.now()
        self.modified = datetime.now()

class SitePathCSS(Base, SerialBase):
    __tablename__ = 'site_view_paths_css'
    path_id = Column(Integer, ForeignKey('site_view_paths.id'),
                     primary_key=True)
    css_id = Column(Integer, ForeignKey('site_css_resources.id'),
                    primary_key=True)

SitePathCSS.path = relationship(SitePath, backref='css')
SitePathCSS.css = relationship(SiteCSS)

class SitePathJS(Base, SerialBase):
    __tablename__ = 'site_view_paths_js'
    path_id = Column(Integer, ForeignKey('site_view_paths.id'),
                     primary_key=True)
    js_id = Column(Integer, ForeignKey('site_js_resources.id'),
                    primary_key=True)

SitePathJS.path = relationship(SitePath, backref='js')
SitePathJS.js = relationship(SiteJS)

# a field type will be text, html, or teacup
class SiteLayoutField(Base, SerialBase):
    __tablename__ = 'site_layout_fields'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    type = Column(Unicode(200))
    

class SiteLayoutModel(Base, SerialBase):
    __tablename__ = 'site_layout_models'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)

# map fields to model
# 
class SiteLayoutModelField(Base, SerialBase):
    __tablename__ = 'site_layout_model_fields'
    model_id = Column(Integer, ForeignKey('site_layout_models.id'),
                     primary_key=True)
    field_id = Column(Integer, ForeignKey('site_layout_fields.id'),
                    primary_key=True)
    content = Column(UnicodeText)
    
SiteLayoutModelField.model = relationship(SiteLayoutModel, backref='fields')
SiteLayoutModelField.field = relationship(SiteLayoutField)


# the page model is a template
# and a set of fields to be
# referenced while rendering the
# template
class SiteWebview(Base, SerialBase):
    __tablename__ = 'site_webviews'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    model_id = Column(ForeignKey('site_layout_models.id'))
    template_id = Column(ForeignKey('site_templates.id'))
    static_resources = Column(PickleType)
    
SiteWebview.model = relationship(SiteLayoutModel)
SiteWebview.template = relationship(SiteTemplate)

    
class SiteWebviewCSS(Base, SerialBase):
    __tablename__ = 'site_webviews_css'
    path_id = Column(Integer, ForeignKey('site_webviews.id'),
                     primary_key=True)
    css_id = Column(Integer, ForeignKey('site_css_resources.id'),
                    primary_key=True)


SiteWebviewCSS.path = relationship(SiteWebview, backref='css')
SiteWebviewCSS.css = relationship(SiteCSS)

# FIXME: the js is really going to be coffee
class SiteWebviewJS(Base, SerialBase):
    __tablename__ = 'site_webviews_js'
    path_id = Column(Integer, ForeignKey('site_webviews.id'),
                     primary_key=True)
    js_id = Column(Integer, ForeignKey('site_js_resources.id'),
                    primary_key=True)

SiteWebviewJS.path = relationship(SiteWebview, backref='js')
SiteWebviewJS.js = relationship(SiteJS)


# everything is coffee script
# these are the main resources for the
# site controlled by admin users.
class SiteAppResource(Base, SerialBase):
    __tablename__ = 'site_app_resources'
    id = Column(Integer, primary_key=True)
    # If paths need to get too deep or
    # named too long, look for another
    # method.
    name = Column(Unicode(80), unique=True)
    content = Column(UnicodeText)
    created = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    modified = Column(DateTime)
    modified_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)

# everything is coffee script
# these are the main resources for the
# apps controlled by other users.
class UserAppResource(Base, SerialBase):
    __tablename__ = 'user_app_resources'
    id = Column(Integer, primary_key=True)
    # If paths need to get too deep or
    # named too long, look for another
    # method.
    name = Column(Unicode(80), unique=True)
    content = Column(UnicodeText)
    created = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    modified = Column(DateTime)
    modified_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)





def populate_images(imagedir='images'):
    session = DBSession()
    from trumpet.managers.admin.images import ImageManager
    im = ImageManager(session)
    import os
    for basename in os.listdir(imagedir):
        filename = os.path.join(imagedir, basename)
        imgfile = file(filename)
        im.add_image(basename, imgfile)
            
def populate_sitetext():
    session = DBSession()
    try:
        with transaction.manager:
            page = SiteText('FrontPage',
                            'This is the front page.', type='tutwiki')
            session.add(page)
    except IntegrityError:
        session.rollback()
        

