import string

import colander
import deform
import vobject

from sqlalchemy.exc import IntegrityError

from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from trumpet.views.base import prepare_layout
from trumpet.views.base import BaseViewer


from trumpet.managers.consultant.contacts import ContactManager

from trumpet.views.consultant.base import prepare_base_layout

phone_re = '\((?P<areacode>[1-9][0-9][0-9])\)-(?P<prefix>[0-9][0-9][0-9])-(?P<suffix>[0-9][0-9][0-9][0-9])'
letters = string.ascii_letters[26:]

    
class FragViewer(BaseViewer):
    def __init__(self, request):
        BaseViewer.__init__(self, request)
        self.contacts = ContactManager(self.request.db)
        
        self._dispatch_table = dict(
            usercontactlist=self.list_user_contacts,
            globalcontactlist=self.list_global_contacts,
            contactlist=self.list_contacts,
            receivedcallscalendar=self.received_calls_calendar,)
        self.context = self.request.matchdict['context']
        self._view = self.context
        self.dispatch()

    def _contact_name_filter(self, query, id):
        Contact = self.contacts.base
        q = self.contacts.query()
        if id != 'ALL':
            q = q.filter(Contact.lastname.like('%s%%' % id))
        return q.order_by(Contact.lastname)

    def _render_contact_list(self, contacts):
        env = dict(contacts=contacts)
        template = 'trumpet:templates/consult/contact-list.mako'
        self.response = self.render(template, env)
        
    def list_user_contacts(self):
        id = self.request.matchdict['id']
        user_id = self.get_current_user_id()
        q = self.contacts.get_by_user_query(user_id)
        q = self._contact_name_filter(q, id)
        contacts = q.all()
        self._render_contact_list(contacts)
        
    def list_global_contacts(self):
        id = self.request.matchdict['id']
        q = self.contacts.get_global_query()
        q = self._contact_name_filter(q, id)
        contacts = q.all()
        self._render_contact_list(contacts)

        
    def list_contacts(self):
        self.list_user_contacts()
        

    def received_calls_calendar(self):
        template = 'trumpet:templates/consult/calendar-phone.mako'
        default_view = 'agendaDay'
        event_source = self.request.route_url(
            'consult_json', context='receivedcalls', id='calls')
        env = dict(default_view=default_view,
                   event_source=event_source,)
        content = self.render(template, env)
        self.response = content
        
        
