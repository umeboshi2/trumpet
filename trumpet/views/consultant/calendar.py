from datetime import datetime, timedelta

import colander
import deform

from pyramid.response import Response

from trumpet.views.base import BasicView


from trumpet.managers.consultant.clients import ClientManager
from trumpet.managers.consultant.contacts import ContactManager
from trumpet.managers.consultant.events import EventManager

from trumpet.views.schema import AddUserSchema
from trumpet.views.schema import deferred_choices, make_select_widget

from trumpet.util import get_regular_users


class AddEventSchema(colander.Schema):
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
    start = colander.SchemaNode(
        colander.DateTime(),
        title='Start Date/Time',
        widget=deform.widget.DateTimeInputWidget()
        )
    end = colander.SchemaNode(
        colander.DateTime(),
        title='End Date/Time',
        widget=deform.widget.DateTimeInputWidget()
        )
    all_day = colander.SchemaNode(
        colander.Boolean(),
        title='All Day',
        widget=deform.widget.CheckboxWidget(),
        )

class CalendarJSONViewer(BasicView):
    def __init__(self, request):
        super(CalendarJSONViewer, self).__init__(request)
        self.events = EventManager(self.request.db)

        self.render_events()


    def _get_start_end_userid(self):
        start = self.request.GET['start']
        end = self.request.GET['end']
        user_id = self.request.session['user'].id
        return start, end, user_id

    def serialize_event(self, event):
        url = self.request.route_url('consult_calendar',
                                     context='view',
                                     id=event.id)
        start = event.start
        end = event.end
        thirty_minutes = timedelta(minutes=30)
        if end - start < thirty_minutes:
            end = start + thirty_minutes
        title = event.title
        id = event.id
        data = dict(id=str(id), title=title,
                    start=start.isoformat(),
                    end=end.isoformat(), url=url)
        return data
    

    def render_events(self):
        start, end, user_id = self._get_start_end_userid()
        serialize = self.serialize_event
        context = self.request.matchdict['context']
        events = self.events.get_events(user_id, start, end, timestamps=True)
        self.response = [serialize(e) for e in events]
        


