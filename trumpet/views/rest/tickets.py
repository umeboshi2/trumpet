import os

from cornice.resource import resource, view

from trumpet.managers.consultant.tickets import TicketManager
from trumpet.views.rest.base import BaseResource, apiroot


cpath = 'consultant/ticket'
cidpath = '%s/{id}' % cpath
@resource(collection_path=os.path.join(apiroot(), cpath),
          path=os.path.join(apiroot(), cidpath))
class TicketResource(BaseResource):
    def __init__(self, request):
        super(TicketResource, self).__init__(request)
        self.mgr = TicketManager(request.db)

    # FIXME: use parameters to filter query
    def collection_get(self):
        g = self.request.GET
        user_id = self.get_current_user_id()
        predefined = False
        start = None
        end = None
        if 'predefined' in g:
            predefined = True
        # if start and end are there, they
        # should be timestamps from fullcalendar
        if 'start' in g and 'end' in g:
            start = g['start']
            end = g['end']
        # this is ugly
        if predefined:
            qtype = g['predefined']
            predefined_types = ['assigned', 'delegated', 'unread', 'pending',
                                'closed']
            if qtype not in predefined_types:
                raise RuntimeError, "Bad predefined type: %s" % qtype
            rangekw = dict(start=start, end=end, timestamps=True)
            methodname = 'get_%s' % qtype
            method = getattr(self.mgr, methodname)
            tickets = method(user_id, **rangekw)
        else:
            tickets = self.mgr.all()
        tlist = [t.serialize() for t in tickets]
        return dict(data=tlist, result='success')
    
    

    # this opens a new ticket
    def collection_post(self):
        j = self.request.json
        user_id = self.get_current_user_id()
        title = j['title']
        description = j['description']
        handler_id = None
        if 'handler_id' in j:
            handler_id = j['handler_id']
        t = self.mgr.open(user_id, title, description,
                          handler_id=handler_id)
        return data(t.serialize(), result='success')
    
    def put(self):
        j = self.request.json
        user_id = self.get_current_user_id()
        ticket_id = self.request.matchdict['id']
        if 'action' not in j:
            raise RuntimeError, "No action defined."
        action = j['action']
        status = j['status']
        reason = j['reason']
        handler_id = j['handler_id']
        description = None
        if 'description' in j:
            description = j['description']
        c = self.mgr.update_ticket(ticket_id, user_id, status,
                                   reason, handler_id,
                                   description=description)
        return data(c.serialize(), result='success')
    
