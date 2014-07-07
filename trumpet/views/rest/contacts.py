import os

from pyramid.response import Response
from cornice.resource import resource, view
import vobject

from trumpet.security import encrypt_password
from trumpet.managers.consultant.contacts import ContactManager
from trumpet.views.rest.base import BaseManagerResource, apiroot
from trumpet.views.base import BasicView

@resource(collection_path=os.path.join(apiroot(), 'consultant/contact'),
          path=os.path.join(apiroot(), 'consultant/contact/{id}'))
class ContactResource(BaseManagerResource):
    def __init__(self, request):
        super(ContactResource, self).__init__(request)
        self.mgr = ContactManager(request.db)

    def collection_get(self):
        contacts = [c.serialize() for c in self.mgr.all()]
        return dict(data=contacts, result='success')
    

    def collection_post(self):
        j = self.request.json
        user_id = self.get_current_user_id()
        firstname = j['firstname']
        lastname = j['lastname']
        email = j['email']
        phone = j['phone']
        c = self.mgr.add_contact(user_id, firstname, lastname, email, phone)
        # FIXME
        self.mgr.make_global(c.id)
        return dict(data=c.serialize(), result='success')
    
    def put(self):
        id = self.request.matchdict['id']

    
###############################
# Import/Export Contacts
###############################

class ContactDataResource(BasicView):
    def __init__(self, request):
        super(ContactDataResource, self).__init__(request)
        self.mgr = ContactManager(self.request.db)

    def _export_contact(self, id, filename=None):
        vcf = self.mgr.export_contact(id)
        r = Response(content_type='text/vcard',
                     body=vcf.serialize())
        if filename is None:
            filename = 'contact-%05d.vcf' % id
        d = 'attachment; filename="%s"' % filename
        r.content_disposition = d
        self.response = r
        
    def _import_contacts(self):
        raise RuntimeError, "not implemented"
        filename = self.request.POST['vcf'].filename
        ifile = self.request.POST['vcf'].file
        stream = ifile.read()
        count = 0
        excluded = []
        for card in vobject.readComponents(stream):
            cfields = parse_vcard_object(card)
            
        
    
