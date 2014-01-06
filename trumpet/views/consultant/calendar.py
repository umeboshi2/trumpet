from datetime import datetime, timedelta

import colander
import deform

from pyramid.response import Response

from trumpet.views.base import render_rst

from trumpet.views.base import prepare_layout
from trumpet.views.base import BaseViewer


from trumpet.managers.consultant.clients import ClientManager
from trumpet.managers.consultant.contacts import ContactManager
from trumpet.managers.consultant.events import EventManager

from trumpet.views.schema import AddUserSchema
from trumpet.views.schema import deferred_choices, make_select_widget

from trumpet.views.consultant.base import prepare_base_layout
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

class CalendarJSONViewer(BaseViewer):
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
        


def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'Calendar'
    layout.header = 'Calendar'
    layout.subheader = 'Calendar Area'
    

    

class CalendarViewer(BaseViewer):
    def __init__(self, request):
        BaseViewer.__init__(self, request)
        prepare_main_layout(self.request)
        self.clients = ClientManager(self.request.db)
        self.contacts = ContactManager(self.request.db)
        self.events = EventManager(self.request.db)
        self._dispatch_table = dict(
            list=self.list_events,
            add=self.add_event,
            delete=self.delete_event,
            confirmdelete=self.confirm_delete_event,
            view=self.view_event,
            export=self.export_event,
            manageusers=self.manage_users,
            detachuser=self.detach_user,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        self.dispatch()

    def _check_authorized(self, event):
        user_id = self.request.session['user'].id
        if user_id == event.created_by_id:
            return True
        event_user_ids = [u.user_id for u in event.users]
        return user_id in event_user_ids
    
    def list_events(self):
        # setup widgetbox
        template = 'trumpet:templates/msl/draggable-event-widget.mako'
        env = dict()
        self.layout.widgetbox = self.render(template, env)
        
        template = 'trumpet:templates/consult/calendar-main.mako'
        env = dict()
        self.layout.content = self.render(template, env)
        self.layout.resources.planevent_calendar_view.need()

    def _add_event_form_submitted(self, form):
        controls = self.request.POST.items()
        self.layout.subheader = "add event form submitted"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        user_id = self.get_current_user_id()
        if data['description'] is colander.null:
            data['description'] = ''
        title = data['title']
        start = data['start']
        end = data['end']
        description = data['description']
        all_day = data['all_day']
        self.events.add_event(title, start, end, description, all_day, user_id)
        self.layout.content = 'Event Created!'
        
    def add_event(self):
        schema = AddEventSchema()
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            self._add_event_form_submitted(form)
        else:
            formdata = dict()
            formdata.update(self.request.POST)
            dtformat = '%Y-%m-%d %H:%M:%S'
            start = None
            if 'start' in formdata:
                start = datetime.strptime(formdata['start'], dtformat)
                formdata['start'] = start
            if 'end' in formdata:
                # sometimes end is null
                try:
                    end = datetime.strptime(formdata['end'], dtformat)
                    formdata['end'] = end
                except ValueError:
                    formdata['end'] = start + timedelta(hours=1)
            all_day = self.request.POST['allDay']
            if all_day == 'false':
                formdata['all_day'] = False
            else:
                formdata['all_day'] = True
            self.layout.footer = all_day
            rendered = form.render(formdata)
            self.layout.content = rendered
            self.layout.subheader = 'Add an Event'
            
        
            
    def view_event(self):
        id = int(self.request.matchdict['id'])
        event = self.events.get(id)
        template = 'trumpet:templates/msl/view-calendar-event.mako'
        env = dict(event=event)
        rendered = self.render(template, env)
        self.layout.content = rendered
        

    def export_event(self):
        id = int(self.request.matchdict['id'])
        ical = self.events.export_ical(id)
        r = Response(content_type='text/calendar',
                     body=ical.serialize())
        filename = 'event-%04d.ics' % id
        r.content_disposition = 'attachment; filename="%s"' % filename
        self.response = r
        
    
    def manage_users(self):
        id = int(self.request.matchdict['id'])
        event = self.events.get(id)
        if not self._check_authorized(event):
            self.layout.content = "unavailable"
            return
        users = event.users
        event_user_ids = [u.user_id for u in users]
        template = 'trumpet:templates/msl/view-calendar-event-users.mako'
        rst = render_rst
        schema = AddUserSchema()
        all_users = get_regular_users(self.request)
        available = [u for u in all_users if u.id not in event_user_ids]
        available = [u for u in available if u.id != event.created_by_id]
        choices = [(u.id, u.username) for u in available]
        schema['user'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        if 'submit' in self.request.POST:
            self._manage_users_form_submitted(form)
        else:
            formdata = dict()
            env = dict(event=event, users=users, form=form, rst=rst)
            content = self.render(template, env)
            self.layout.content = content
            
    def _manage_users_form_submitted(self, form):
        event_id = int(self.request.matchdict['id'])
        controls = self.request.POST.items()
        self.layout.subheader = "Event user submitted to database"
        try:
            data = form.validate(controls)
        except deform.ValidationFailure, e:
            self.layout.content = e.render()
            return
        user_id = data['user']
        self.events.attach_user(event_id, user_id)
        self.response = HTTPFound(self.url(context='manageusers', id=event_id))
        
    def detach_user(self):
        event_id, user_id = self.request.matchdict['id'].split('_')
        event_id = int(event_id)
        user_id = int(user_id)
        event = self.events.get(event_id)
        if not self._check_authorized(event):
            self.layout.content = "unavailable"
            return
        self.events.detach_user(event_id, user_id)
        self.response = HTTPFound(self.url(context='manageusers', id=event_id))
        
        

    def delete_event(self):
        pass

    def confirm_delete_event(self):
        pass
    
