import os
from datetime import datetime, timedelta

import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from sqlalchemy import func

from trumpet.managers.util import convert_range_to_datetime

from trumpet.models.consultant import Description
from trumpet.models.consultant import Ticket, TicketCurrentStatus
from trumpet.models.consultant import TicketStatusChange
from trumpet.models.consultant import TicketDocument

class DescriptionManager(object):
    def __init__(self, session):
        self.session = session

    def query(self):
        return self.session.query(Description)

    def new(self, text):
        with transaction.manager:
            d = Description()
            d.text = text
            self.session.add(d)
        return self.session.merge(d)

    def get(self, id):
        return self.query().get(id)
    
    def update(self, text):
        with transaction.manager:
            try:
                d = self.session.query(Description).filter_by(text=text).one()
            except NoResultFound:
                d = Description()
                d.text = text
                self.session.add(d)
                d = self.session.merge(d)
        return d
    
class TicketManager(object):
    def __init__(self, session):
        self.session = session
        self.descriptions = DescriptionManager(self.session)

    def query(self):
        return self.session.query(Ticket)

    def get(self, id):
        return self.query().get(id)
    
    def open(self, user_id, title, description, handler_id=None):
        if handler_id is None:
            handler_id = user_id
        with transaction.manager:
            now = datetime.now()
            d = self.descriptions.new(description)
            t = Ticket()
            t.title = title
            t.description_id = d.id
            t.created = now
            self.session.add(t)
            ticket = self.session.merge(t)
            change = TicketStatusChange()
            change.ticket_id = ticket.id
            change.status = 'opened'
            change.reason = "New Ticket"
            change.description_id = d.id
            change.changed = now
            change.changed_by_id = user_id
            change.handler_id = handler_id
            self.session.add(change)
            change = self.session.merge(change)
            current = TicketCurrentStatus()
            current.ticket_id = ticket.id
            current.last_change_id = change.id
            current.created = ticket.created
            current.last_change = change.changed
            current.status = change.status
            current.changed_by_id = user_id
            current.handler_id = handler_id
            self.session.add(current)
        return self.session.merge(ticket)
    


    def update_ticket(self, ticket_id, user_id, status, reason, handler_id,
                      description=None):
        now = datetime.now()
        with transaction.manager:
            ticket = self.get(ticket_id)
            change = TicketStatusChange()
            change.ticket_id = ticket_id
            change.status = status
            change.reason = reason
            change.changed = now
            change.changed_by_id = user_id
            change.handler_id = handler_id
            if description is None:
                change.description_id = ticket.description_id
            self.session.add(change)
            change = self.session.merge(change)
            current = self.session.query(TicketCurrentStatus).get(ticket_id)
            current.last_change = now
            current.last_change_id = change.id
            current.status = status
            current.changed_by_id = user_id
            current.handler_id = handler_id
            current = self.session.merge(current)
        return self.session.merge(change)

    def all(self):
        return self.query().all()

    def status(self, ticket_id):
        q = self.session.query(TicketCurrentStatus)
        q = q.filter_by(ticket_id=ticket_id)
        return q.one()

    def get_status(self, ticket_id):
        s = self.status(ticket_id)
        return s.status
    
    def _range_filter(self, query, start, end):
        "start and end are datetime objects"
        query = query.filter(TicketCurrentStatus.last_change >= start)
        query = query.filter(TicketCurrentStatus.last_change <= end)
        return query
    
    def get_current_status_range(self, start, end, timestamps=False):
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(TicketCurrentStatus)
        q = self._range_filter(q, start, end)
        return q.all()
    
    def get_current_status_range_ts(self, start, end):
        return self.get_current_status_range(start, end, timestamps=True)

    def _basic_query(self, user_id, 
                     start=None, end=None, timestamps=False):
        q = self.session.query(TicketCurrentStatus)
        q = q.filter_by(handler_id=user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._range_filter(q, start, end)
        return q
    

    def get_assigned_query(self, user_id,
                           start=None, end=None, timestamps=False):
        q = self._basic_query(user_id, start=start, end=end,
                              timestamps=timestamps)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q

    def get_assigned(self, user_id,
                     start=None, end=None, timestamps=False):
        q = self.get_assigned_query(user_id, start=start, end=end,
                                    timestamps=timestamps)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q.all()

    def get_delegated_query(self, user_id,
                            start=None, end=None, timestamps=False):
        q = self.session.query(TicketCurrentStatus)
        q = q.filter_by(changed_by_id=user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        q = q.filter(TicketCurrentStatus.handler_id != user_id)
        return q

    def get_delegated(self, user_id,
                      start=None, end=None, timestamps=False):
        q = self.get_delegated_query(user_id, start=start, end=end,
                                     timestamps=timestamps)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q.all()

    def _get_by_status_query(self, user_id, status,
                             start=None, end=None, timestamps=False):
        q = self._basic_query(user_id, start=start, end=end,
                              timestamps=timestamps)
        q = q.filter_by(status=status)
        return q
    
    def _get_by_status(self, user_id, status,
                       start=None, end=None, timestamps=False):
        q = self._get_by_status_query(user_id, status, start=start, end=end,
                                      timestamps=timestamps)
        return q.all()

    def get_unread(self, user_id,
                   start=None, end=None, timestamps=False):
        return self._get_by_status(user_id, 'opened',
                                   start=start, end=end, timestamps=timestamps)

    def get_pending(self, user_id,
                   start=None, end=None, timestamps=False):
        return self._get_by_status(user_id, 'pending',
                                   start=start, end=end, timestamps=timestamps)
    
    def get_closed(self, user_id,
                   start=None, end=None, timestamps=False):
        return self._get_by_status(user_id, 'closed',
                                   start=start, end=end, timestamps=timestamps)
    

    def attach_document(self, ticket_id, doc_id, user_id):
        document = self.session.query(TicketDocument).get((ticket_id, doc_id))
        if document is None:
            with transaction.manager:
                now = datetime.now()
                cd = TicketDocument()
                cd.ticket_id = ticket_id
                cd.doc_id = doc_id
                cd.attached = now
                cd.attached_by_id = user_id
                self.session.add(cd)
            document = self.session.merge(cd)
            reason = "Added Document %d to Ticket" % doc_id
            status = "pending"
            current = self.session.query(TicketCurrentStatus).get(ticket_id)
            handler_id = current.handler_id
            self.update_ticket(ticket_id, user_id, status, reason, handler_id)
        return document
        


