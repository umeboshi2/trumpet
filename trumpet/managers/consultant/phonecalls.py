import os
from datetime import datetime, timedelta

import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from sqlalchemy import func

from trumpet.managers.util import convert_range_to_datetime

#FIXME: better module name
from trumpet.models.consultant import Ticket, TicketCurrentStatus
from trumpet.models.consultant import PhoneCall

from trumpet.managers.consultant.tickets import TicketManager



class PhoneCallManager(object):
    def __init__(self, session):
        self.session = session
        self.tickets = TicketManager(self.session)
        
    def query(self):
        q = self.session.query(PhoneCall, TicketCurrentStatus)
        q = q.filter(PhoneCall.ticket_id == TicketCurrentStatus.ticket_id)
        return q
    
    def get(self, id):
        return self.session.query(PhoneCall).get(id)

    def get_status(self, id):
        q = self.query().filter(PhoneCall.id == id)
        return q.one()
    

    
    def new_call(self, received, caller, number,
                 callee_id, received_by_id, title, description):
        with transaction.manager:
            now = datetime.now()
            # the ticket is opened by the receiver
            # and then handled by the callee
            ticket = self.tickets.open(received_by_id,
                                       title, description, callee_id)
            pc = PhoneCall()
            pc.received = received
            pc.caller = caller
            pc.number = number
            pc.callee_id = callee_id
            pc.received_by_id = received_by_id
            pc.ticket_id = ticket.id
            self.session.add(pc)
        return self.session.merge(pc)

    def _received_range_filter(self, query, start, end):
        query = query.filter(PhoneCall.received >= start)
        query = query.filter(PhoneCall.received <= end)
        return query

    def _lastchange_range_filter(self, query, start, end):
        query = query.filter(TicketCurrentStatus.last_change >= start)
        query = query.filter(TicketCurrentStatus.last_change <= end)
        return query
    
    def get_taken_calls(self, user_id, start=None,
                        end=None, timestamps=False):
        q = self.query()
        q = q.filter(PhoneCall.received_by_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q.all()

    def get_received_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(PhoneCall.callee_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q.all()

    def get_assigned_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(TicketCurrentStatus.handler_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status != 'closed')
        return q.all()

    def get_unread_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(TicketCurrentStatus.handler_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status == 'opened')
        return q.all()

    def get_pending_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(TicketCurrentStatus.handler_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status == 'pending')
        return q.all()
    
    def get_closed_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(TicketCurrentStatus.handler_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status == 'closed')
        return q.all()
    

    def get_delegated_calls(self, user_id, start=None,
                           end=None, timestamps=False):
        q = self.query()
        q = q.filter(PhoneCall.callee_id == user_id)
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._received_range_filter(q, start, end)
        q = q.filter(TicketCurrentStatus.status == 'pending')
        q = q.filter(TicketCurrentStatus.changed_by_id != user_id)
        return q.all()
                            

class PhoneCallAdminManager(PhoneCallManager):
    def __init__(self, session):
        super(PhoneCallAdminManager, self).__init__(session)

    def _filter_by_status_name(self, status):
        status_id = self.stypes.get_id(status)
        q = self.session.query(TicketCurrentStatus)
        return q.filter(TicketCurrentStatus.status == status_id)

    def _filter_by_status_name_range(self,
                                     status, start, end,
                                     timestamps=False):
        status_id = self.stypes.get_id(status)
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(TicketCurrentStatus)
        q = self._last_change_range(q, start, end)
        return q.filter(TicketCurrentStatus.status == status_id)

    def get_unread_calls(self, start, end, timestamps=False):
        q = self._filter_by_status_name_range('opened', start, end,
                                              timestamps=timestamps)
        return q.all()

    def get_all_unread_calls(self):
        q = self._filter_by_status_name('opened')
        return q.all()

    def get_pending_calls(self, start, end, timestamps=False):
        q = self._filter_by_status_name_range('pending', start, end,
                                              timestamps=timestamps)
        return q.all()

    def get_all_pending_calls(self):
        q = self._filter_by_status_name('pending')
        return q.all()

    def get_closed_calls(self, start, end, timestamps=False):
        q = self._filter_by_status_name_range('closed', start, end,
                                              timestamps=timestamps)
        return q.all()

    def get_all_closed_calls(self):
        q = self._filter_by_status_name('closed')
        return q.all()
    
    
class ScannedDocumentsManager(object):
    def __init__(self, session):
        self.session = session
        self.directory = None
        
    def query(self):
        q = self.session.query(ScannedDocument)
        return q
    
    def get(self, id):
        return self.query().get(id)

    def set_scans_directory(self, directory):
        self.directory = directory

    def insert_scanned_file(self, filename):
        fullname = os.path.join(self.directory, filename)
        # file must fit in memory
        content = file(fullname).read()
        created = datetime_from_pdf_filename(filename)
        with transaction.manager:
            f = File()
            f.content = content
            self.session.add(f)
            f = self.session.merge(f)
            s = ScannedDocument()
            s.created = created
            s.name = filename
            s.file_id = f.id
            self.session.add(s)
            s = self.session.merge(s)
        return s
    
        
    def get_latest(self):
        try:
            q = self.session.query(ScannedDocument)
            q = q.order_by(ScannedDocument.created.desc())
            return q.first()
        except NoResultFound:
            return None
        

    def update_database(self):
        filenames = get_scanned_filenames(self.directory)
        latest = self.get_latest()
        for filename in filenames:
            dt = datetime_from_pdf_filename(filename)
            if latest is None or dt > latest.created:
                self.insert_scanned_file(filename)

    def _range_filter(self, query, start, end):
        query = query.filter(ScannedDocument.created >= start)
        query = query.filter(ScannedDocument.created <= end)
        return query
    
    def get_documents(self, start, end, timestamps=False):
        if timestamps:
            start, end = convert_range_to_datetime(start, end)
        q = self.session.query(ScannedDocument)
        q = self._range_filter(q, start, end)
        return q.all()
    
                
    
