import urlparse
from datetime import datetime, timedelta
from ConfigParser import NoSectionError, DuplicateSectionError

from pyramid.httpexceptions import HTTPFound

from sqlalchemy.orm.exc import NoResultFound

import colander
import deform

from trumpet.views.base import BasicView

from trumpet.managers.consultant.tickets import TicketManager
from trumpet.managers.consultant.phonecalls import PhoneCallManager

from trumpet.views.schema import deferred_choices, make_select_widget

from trumpet.models.usergroup import User
from trumpet.models.consultant import PhoneCall

from trumpet.managers.util import send_email_through_smtp_server, make_email_message


class NewTicketSchema(colander.Schema):
    handler = colander.SchemaNode(
        colander.Integer(),
        title='Handler',
        widget=deferred_choices,
        description='This is the user that will handle this ticket',
        )
    title = colander.SchemaNode(
        colander.String(),
        title='Title',
        )
    description = colander.SchemaNode(
        colander.String(),
        title='Description',
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        missing=colander.null,
        )
    send_textmsg = colander.SchemaNode(
        colander.Boolean(),
        title="Send text message to handler's cellphone",
        widget=deform.widget.CheckboxWidget(),
        )
    
reason_description = """\
You can instruct another user to handle the ticket by
 changing the handler of this ticket and typing the instructions
 in this area.
"""
class UpdateTicketSchema(colander.Schema):
    status = colander.SchemaNode(
        colander.Integer(),
        title='New Status',
        widget=deferred_choices,
        )
    handler = colander.SchemaNode(
        colander.Integer(),
        title='Handler',
        widget=deferred_choices,
        description='This is the user that will handle this ticket',
        )
    reason = colander.SchemaNode(
        colander.String(),
        title='Reason',
        description=reason_description,
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        )
    

    
class TicketFrag(BasicView):
    def __init__(self, request):
        super(TicketFrag, self).__init__(request)
        self._template = 'trumpet:templates/msl/list-tickets.mako'
        self.tickets = TicketManager(self.request.db)
        tkt_types = ['assigned', 'delegated', 'unread',
                     'pending', 'closed']
        self.dtformat = '%A - %B %d %H:%m'
        self.env = dict(dtformat=self.dtformat)
        self.render_ticket_list()
        
    def _getuserid(self):
        return self.request.session['user'].id

    def _render_tickets(self, tkt_type):
        user_id = self._getuserid()
        method = getattr(self.tickets, 'get_%s' % tkt_type)
        tlist = method(user_id)
        env = self.env.update(tlist=tlist)
        self.response = self.render(self._template, self.env)
        
    def render_ticket_list(self):
        context = self.request.matchdict['context']
        self._render_tickets(context)
        
class BaseJSONViewer(BasicView):
    def __init__(self, request):
        super(BaseJSONViewer, self).__init__(request)
        self.tickets = TicketManager(self.request.db)
        self.context = None
        self._dispatch_table = dict(
            assigned_tickets=self.get_assigned_tickets,
            delegated_tickets=self.get_delegated_tickets,
            unread_tickets=self.get_unread_tickets,
            pending_tickets=self.get_pending_tickets,
            closed_tickets=self.get_closed_tickets,
            )

        self.context = self.request.matchdict['context']
        self._view = self.context
        self.dispatch()

    def serialize_ticket_current_status_for_calendar(self, cstatus):
        url = self.request.route_url('msl_tickets',
                                     context='viewticket',
                                     id=cstatus.ticket_id)
        status = cstatus.status
        title = cstatus.ticket.title
        data = dict(id=cstatus.ticket_id,
                    #start=cstatus.last_change.isoformat(),
                    start=cstatus.ticket.created.isoformat(),
                    end=cstatus.last_change.isoformat(),
                    title=title,
                    url=url)
        if status == 'pending':
            data['color'] = 'blue'
        return data

    def _get_start_end_userid(self):
        start = self.request.GET['start']
        end = self.request.GET['end']
        user_id = self.request.session['user'].id
        return start, end, user_id
    
    def get_assigned_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        tickets = self.tickets.get_assigned(user_id, start=start, end=end,
                                            timestamps=True)
        tlist = []
        for cstatus in tickets:
            tdata = serialize(cstatus)
            tlist.append(tdata)
        self.response = tlist
        
    def get_delegated_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        tickets = self.tickets.get_delegated(user_id, start=start, end=end,
                                            timestamps=True)
        tlist = []
        for cstatus in tickets:
            tdata = serialize(cstatus)
            tlist.append(tdata)
        self.response = tlist
        
    def get_unread_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        tickets = self.tickets.get_unread(user_id, start=start, end=end,
                                            timestamps=True)
        tlist = []
        for cstatus in tickets:
            tdata = serialize(cstatus)
            tlist.append(tdata)
        self.response = tlist

    def get_pending_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        tickets = self.tickets.get_pending(user_id, start=start, end=end,
                                            timestamps=True)
        tlist = []
        for cstatus in tickets:
            tdata = serialize(cstatus)
            tlist.append(tdata)
        self.response = tlist

    def get_closed_tickets(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_ticket_current_status_for_calendar
        tickets = self.tickets.get_closed(user_id, start=start, end=end,
                                            timestamps=True)
        tlist = []
        for cstatus in tickets:
            tdata = serialize(cstatus)
            tlist.append(tdata)
        self.response = tlist

class TicketJSONViewer(BaseJSONViewer):
    def __init__(self, request):
        super(TicketJSONViewer, self).__init__(request)
        
