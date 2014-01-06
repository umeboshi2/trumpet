import os
from datetime import datetime, timedelta

import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from sqlalchemy import func

from trumpet.managers.util import convert_range_to_datetime

#FIXME: better module name
from trumpet.models.consultant import Description
from trumpet.models.consultant import Ticket, TicketCurrentStatus
from trumpet.models.consultant import TicketStatusChange

from trumpet.models.consultant import Case, CaseTicket, CaseDocument
from trumpet.models.consultant import UnassignedDocument
from trumpet.models.consultant import CaseUser
from trumpet.models.consultant import CaseStatusChange, CaseCurrentStatus

from trumpet.managers.consultant.tickets import DescriptionManager
    
class CaseManager(object):
    def __init__(self, session):
        self.session = session
        self.descriptions = DescriptionManager(self.session)

    def query(self):
        return self.session.query(Case)

    def get(self, id):
        return self.query().get(id)
    
    def open_case(self, name, description, client_id,
                  user_id, handler_id=None):
        if handler_id is None:
            handler_id = user_id
        d = self.descriptions.new(description)
        with transaction.manager:
            now = datetime.now()
            c = Case()
            c.name = name
            c.client_id = client_id
            c.description_id = d.id
            c.created = now
            c.created_by_id = user_id
            self.session.add(c)
            c = self.session.merge(c)
            change = CaseStatusChange()
            change.case_id = c.id
            change.status = 'opened'
            change.reason = 'New Case'
            change.description_id = d.id
            change.changed = now
            change.changed_by_id = user_id
            change.handler_id = handler_id
            self.session.add(change)
            change = self.session.merge(change)
            current = CaseCurrentStatus()
            current.case_id = c.id
            current.last_change_id = change.id
            current.created = c.created
            current.last_change = change.changed
            current.status = change.status
            current.changed_by_id = user_id
            current.handler_id = handler_id
            self.session.add(current)
            cu = CaseUser()
            cu.case_id = c.id
            cu.user_id = user_id
            self.session.add(cu)
        return self.session.merge(c)

    def update_case(self, case_id, user_id, status, reason, handler_id,
                    description=None):
        with transaction.manager:
            now = datetime.now()
            case = self.get(case_id)
            change = CaseStatusChange()
            change.case_id = case_id
            change.status = status
            change.reason = reason
            change.changed = now
            change.changed_by_id = user_id
            change.handler_id = handler_id
            if description is None:
                change.description_id = case.description_id
            self.session.add(change)
            change = self.session.merge(change)
            current = self.session.query(CaseCurrentStatus).get(case_id)
            current.last_change = now
            current.last_change_id = change.id
            current.status = status
            current.changed_by_id = user_id
            current.handler_id = handler_id
            current = self.session.merge(current)
        return self.session.merge(change)
    
    
    def attach_ticket(self, case_id, ticket_id, user_id):
        ticket = self.session.query(CaseTicket).get((case_id, ticket_id))
        if ticket is None:
            with transaction.manager:
                now = datetime.now()
                ct = CaseTicket()
                ct.case_id = case_id
                ct.ticket_id = ticket_id
                ct.attached = now
                ct.attached_by_id = user_id
                self.session.add(ct)
            ticket = self.session.merge(ct)
            reason = "Added Ticket to Case"
            status = "pending"
            current = self.session.query(CaseCurrentStatus).get(case_id)
            handler_id = current.handler_id
            self.update_case(case_id, user_id, status, reason, handler_id)
        return ticket

    def get_tickets(self, case_id):
        q = self.session.query(Ticket)
        q = q.filter(CaseTicket.ticket_id == Ticket.id)
        q = q.filter(CaseTicket.case_id == case_id)
        return q.all()
    
        
    def attach_document(self, case_id, doc_id, user_id):
        document = self.session.query(CaseDocument).get((case_id, doc_id))
        if document is None:
            with transaction.manager:
                now = datetime.now()
                cd = CaseDocument()
                cd.case_id = case_id
                cd.doc_id = doc_id
                cd.attached = now
                cd.attached_by_id = user_id
                self.session.add(cd)
                udoc = self.session.query(UnassignedDocument).get(doc_id)
                self.session.delete(udoc)
            document = self.session.merge(cd)
            reason = "Added Document to Case"
            status = "pending"
            current = self.session.query(CaseCurrentStatus).get(case_id)
            handler_id = current.handler_id
            self.update_case(case_id, user_id, status, reason, handler_id)
        return document
        
    def attach_user(self, case_id, user_id):
        user = self.session.query(CaseUser).get((case_id, user_id))
        if user is None:
            with transaction.manager:
                now = datetime.now()
                cu = CaseUser()
                cu.case_id = case_id
                cu.user_id = user_id
                self.session.add(cu)
            user = self.session.merge(cu)
            reason = "Added User to Case"
            status = "pending"
            current = self.session.query(CaseCurrentStatus).get(case_id)
            handler_id = current.handler_id
            self.update_case(case_id, user_id, status, reason, handler_id)
        return user    

    def detach_user(self, case_id, user_id):
        with transaction.manager:
            q = self.session.query(CaseUser)
            q = q.filter(Case.id == CaseUser.case_id)
            q = q.filter(CaseUser.case_id == case_id)
            q = q.filter(Case.created_by_id != CaseUser.user_id)
            q = q.filter(CaseUser.user_id == user_id)
            deleted = False
            try:
                cu = q.one()
                self.session.delete(cu)
                deleted = True
            except NoResultFound:
                pass
        if deleted:
            reason = "Removed User from Case"
            status = "pending"
            current = self.session.query(CaseCurrentStatus).get(case_id)
            handler_id = current.handler_id
            self.update_case(case_id, user_id, status, reason, handler_id)

    def status(self, case_id):
        q = self.session.query(CaseCurrentStatus)
        q = q.filter_by(case_id=case_id)
        return q.one()

    def get_status(self, case_id):
        s = self.status(case_id)
        return s.status

    def _range_filter(self, query, start, end):
        "start and end are datetime objects"
        query = query.filter(CaseCurrentStatus.last_change >= start)
        query = query.filter(CaseCurrentStatus.last_change <= end)
        return query
    
    def get_current_status_range(self, start, end, timestamps=False):
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(CaseCurrentStatus)
        q = self._range_filter(q, start, end)
        return q.all()    

    def _basic_query(self, user_id, 
                     start=None, end=None, timestamps=False):
        q = self.session.query(CaseCurrentStatus)
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
        q = q.filter(CaseCurrentStatus.status != 'closed')
        return q

    def get_assigned(self, user_id,
                     start=None, end=None, timestamps=False):
        q = self.get_assigned_query(user_id, start=start, end=end,
                                    timestamps=timestamps)
        return q.all()

    def get_delegated_query(self, user_id,
                            start=None, end=None, timestamps=False):
        q = self.session.query(CaseCurrentStatus)
        q = q.filter_by(changed_by_id=user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._range_filter(q, start, end)
        q = q.filter(CaseCurrentStatus.status != 'closed')
        q = q.filter(CaseCurrentStatus.handler_id != user_id)
        return q

    def get_delegated(self, user_id,
                      start=None, end=None, timestamps=False):
        q = self.get_delegated_query(user_id, start=start, end=end,
                                     timestamps=timestamps)
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
    

    def get_accessible(self, user_id,
                   start=None, end=None, timestamps=False):
        q = self.session.query(CaseCurrentStatus)
        q = q.filter(CaseUser.case_id == CaseCurrentStatus.case_id)
        q = q.filter(CaseUser.user_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._range_filter(q, start, end)
        q = q.filter(CaseCurrentStatus.status != 'closed')
        return q.all()
    

