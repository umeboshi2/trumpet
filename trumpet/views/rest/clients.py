import os

from cornice.resource import resource, view

from trumpet.security import encrypt_password
from trumpet.managers.consultant.clients import ClientManager
from trumpet.views.rest.base import BaseResource, apiroot



@resource(collection_path=os.path.join(apiroot(), 'consultant/client'),
          path=os.path.join(apiroot(), 'consultant/client/{id}'))
class ClientResource(BaseResource):
    def __init__(self, request):
        super(ClientResource, self).__init__(request)
        self.mgr = ClientManager(request.db)

    def collection_get(self):
        clients = [c.serialize() for c in self.mgr.all()]
        return dict(data=clients, result='success')
    

    def collection_post(self):
        j = self.request.json
        contact_id = j['contact_id']
        name = j['name']
        address = None
        if 'address' in j:
            address = j['address']
        description = None
        if 'description' in j:
            description = j['description']
        c = self.mgr.add(name, contact_id,
                         address=address, description=description)
        return dict(data=c.serialize(), result='success')
    
    def put(self):
        id = self.request.matchdict['id']
        raise RuntimeError, "Not implemented."
    
