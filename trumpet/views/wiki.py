import re
from datetime import datetime

import transaction
from docutils.core import publish_parts

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config

import colander
import deform

from trumpet.models.base import DBSession
from trumpet.models.sitecontent import SiteText

from base import BaseViewer, BaseMenu
from base import render_rst

# regular expression used to find WikiWords
wikiwords = re.compile(r":\b([A-Z]\w+[A-Z]+\w+)")

EDIT_PAGE_FORM = """<form action="%s" method="post">
          <textarea name="body" rows="10"
                    cols="60">%s</textarea><br/>
          <input type="submit" name="form.submitted" value="Save">
        </form>"""


class EditPageSchema(colander.Schema):
    body = colander.SchemaNode(
        colander.String())
    
def _anchor(href, value):
    return '<a href="%s">%s</a>' % (href, value)


def prepare_main_data(request):
    layout = request.layout_manager.layout
    layout.title = 'Wiki Page'
    layout.header = 'Wiki Page'


class WikiViewer(BaseViewer):
    def __init__(self, request):
        # dispatch table
        self._dispatch_table = dict(view_wiki=self.view_wiki,
                                    view_page=self.view_page,
                                    add_page=self.add_page,
                                    edit_page=self.edit_page,
                                    list_pages=self.list_pages)
        self.route = request.matched_route.name
        self._view = self.route
        super(WikiViewer, self).__init__(request)
        prepare_main_data(self.request)
        menu = BaseMenu()
        menu.set_header('Wiki Menu')
        url = self.request.route_url('view_page', pagename='MainPlan')
        menu.append_new_entry('Main Plan', url)
        url = self.request.route_url('list_pages')
        menu.append_new_entry('List Pages', url)
        self.layout.main_menu = menu
        
    def _anchor(self, href, value):
        return '<a href="%s">%s</a>' % (href, value)

    def view_wiki(self):
        location = self.request.route_url('view_page', pagename='FrontPage')
        self.response = HTTPFound(location=location)

    def view_page(self):
        pagename = self.request.matchdict['pagename']
        session = DBSession()
        page = session.query(SiteText).filter_by(name=pagename).first()
        if page is None:
            location = self.url(route='add_page', pagename=pagename)
            self.response = HTTPFound(location=location)
            return

        def check(match):
            word = match.group(1)
            exists = session.query(SiteText).filter_by(name=word).all()
            if exists:
                url = self.url(route='view_page', pagename=word)
            else:
                url = self.url(route='add_page', pagename=word)
            return self._anchor(url, word)
        # this is a sad "markup" system
        # good for a tutorial, but needs to be better
        # for actual use.
        content = render_rst(page.content)
        content = wikiwords.sub(check, content)

        edit_url = self.url(route='edit_page', pagename=pagename)
        # We should check the session here
        # this is from tutorial, but we need better
        # solution.
        #logged_in = authenticated_userid(self.request)
        l = self.layout
        l.title = "Wiki: %s" % page.name
        l.header = page.name
        l.content = content
        l.footer = self._anchor(edit_url, "Edit Page")
        
    def _add_new_page(self, name):
        session = DBSession()
        body = self.request.params['body']
        with transaction.manager:
            page = SiteText(name, body, type='tutwiki')
            session.add(page)
        


    def _edit_form_submitted(self, name, page=None):
        edit_page = True
        session = DBSession()
        body = self.request.params['body']
        now = datetime.now()
        if page is None:
            edit_page = False
            page = SiteText(name, body, type='tutwiki')
            page.created = now
        else:
            page.content = body
        page.modified = now
        with transaction.manager:
            session.add(page)
        location = self.url(route='view_page', pagename=name)
        self.response = HTTPFound(location=location)        
        
        
            
    def add_page(self):
        name = self.request.matchdict['pagename']
        if 'form.submitted' in self.request.params:
            self._edit_form_submitted(name)
            return
        save_url = self.url(route='add_page', pagename=name)
        # logged_in = authenticated_userid(self.request)
        self.layout.content = EDIT_PAGE_FORM % (save_url, '')
        
    def edit_page(self):
        name = self.request.matchdict['pagename']
        session = DBSession()
        #page = session.query(Page).filter_by(name=name).one()
        page = session.query(SiteText).filter_by(name=name).one()
        if 'form.submitted' in self.request.params:
            self._edit_form_submitted(name, page=page)
            return
        save_url = self.url(route='edit_page', pagename=name)
        #logged_in = authenticated_userid(self.request)
        self.layout.content = EDIT_PAGE_FORM % (save_url, page.content)

    def list_pages(self):
        session = DBSession()
        #pages = session.query(Page).all()
        pages = session.query(SiteText).filter_by(type='tutwiki').all()
        pagelist = []
        for page in pages:
            url = self.url(route='view_page', pagename=page.name)
            anchor = self._anchor(url, page.name)
            pagelist.append('<li>%s</li>' % anchor)
        ul = '<ul>%s</ul>' % '\n'.join(pagelist)
        self.layout.content = ul
