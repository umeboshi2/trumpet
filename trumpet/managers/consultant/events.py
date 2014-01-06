import os
from datetime import datetime, timedelta

import transaction
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from sqlalchemy import func
import vobject

from trumpet.managers.util import convert_range_to_datetime

#FIXME: better module name
from trumpet.models.consultant import Event, EventUser

def make_ical(event):
    dtime = datetime(2001, 1, 1)
    cal = vobject.iCalendar()
    cal.add('vevent')
    cal.vevent.add('summary').value = event.title
    cal.vevent.add('description').value = event.description
    cal.vevent.add('organizer').value = event.created_by.username
    #cal.vevent.add('location').value = event.venue.name
    cal.vevent.add('dtstart').value = event.start
    cal.vevent.add('dtend').value = event.end
    return cal
    

class EventManager(object):
    def __init__(self, session):
        self.session = session

    def query(self):
        return self.session.query(Event)

    def get(self, id):
        return self.query().get(id)

    def add_event(self, title, start, end, description, all_day, user_id):
        now = datetime.now()
        with transaction.manager:
            event = Event(title)
            event.start = start
            event.end = end
            event.start_date = start.date()
            event.start_time = start.time()
            event.end_date = end.date()
            event.end_time = end.time()
            event.title = title
            event.description = description
            event.all_day = all_day
            event.created = now
            event.created_by_id = user_id
            self.session.add(event)
        return self.session.merge(event)

    def update_event(self, event_id,
                     title, start, end, description, all_day, user_id):
        with transaction.manager:
            event = self.get(event_id)
            if event is None:
                raise RuntimeError, "event should be in database"
            if event.created_by_id != user_id:
                raise RuntimeError, "user didn't create event"
            event.start = start
            event.end = end
            event.start_date = start.date()
            event.start_time = start.time()
            event.end_date = end.date()
            event.end_time = end.time()
            event.title = title
            event.description = description
            event.all_day = all_day
            event = self.session.merge(event)
        return event
    

    def all(self):
        return self.query().all()

    def _range_filter(self, query, start, end):
        "start and end are datetime objects"
        query = query.filter(Event.start >= start)
        query = query.filter(Event.start <= end)
        return query

    def _common_range_query(self, start, end, timestamps):
        q = self.query()
        if start is not None:
            if timestamps:
                start, end = convert_range_to_datetime(start, end)
            q = self._range_filter(q, start, end)
        return q
    
    def get_events(self, user_id, start=None, end=None, timestamps=False):
        q = self._common_range_query(start, end, timestamps)
        q = q.filter(Event.created_by_id == user_id)
        return q.all()

    def get_all_events(self, start=None, end=None, timestamps=False):
        q = self._common_range_query(start, end, timestamps)
        return q.all()

    def export_ical(self, id):
        event = self.get(id)
        return make_ical(event)

    def attach_user(self, event_id, user_id, attached_by_id):
        user = self.session.query(EventUser).get((event_id, user_id))
        if user is None:
            with transaction.manager:
                now = datetime.now()
                eu = EventUser()
                eu.event_id = event_id
                eu.user = user_id
                eu.attached = now
                eu.attached_by_id = attached_by_id
                self.session.add(eu)
                
