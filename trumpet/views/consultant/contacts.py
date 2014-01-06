import string

import colander
import deform
import vobject

from sqlalchemy.exc import IntegrityError

from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from trumpet.views.menus import BaseMenu

from trumpet.views.base import prepare_layout
from trumpet.views.base import BaseViewer


from trumpet.managers.consultant.contacts import ContactManager

from trumpet.views.consultant.base import prepare_base_layout


phone_re = '\((?P<areacode>[1-9][0-9][0-9])\)-(?P<prefix>[0-9][0-9][0-9])-(?P<suffix>[0-9][0-9][0-9][0-9])'
letters = string.ascii_letters[26:]

class AddContactSchema(colander.Schema):
    firstname = colander.SchemaNode(
        colander.String(),
        title = 'First Name',
        )
    lastname = colander.SchemaNode(
        colander.String(),
        title = 'Last Name',
        missing=colander.null,
        )
    email = colander.SchemaNode(
        colander.String(),
        validator=colander.Email(),
        title='Email Address',
        missing=colander.null,
        )
    phone = colander.SchemaNode(
        colander.String(),
        title='Phone Number',
        widget=deform.widget.TextInputWidget(mask='(999)-999-9999',
                                      mask_placeholder='0'),
        missing=colander.null,
        )

def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'Consultant Contacts'
    layout.header = 'Consultant Contacts'
    layout.subheader = 'Contacts Area'
    


class ContactViewer(BaseViewer):
    def __init__(self, request):
        BaseViewer.__init__(self, request)
        prepare_main_layout(self.request)
        self.contacts = ContactManager(self.request.db)
        self._dispatch_table = dict(
            list=self.list_contacts,
            add=self.add_contact,
            delete=self.delete_contact,
            confirmdelete=self.confirm_delete_contact,
            viewcontact=self.view_contact,
            editcontact=self.edit_contact,
            exportcontact=self.export_contact,
            exportall=self.export_all_contacts,
            importcontact=self.import_contact,
            importsubmit=self.import_contact_submit,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        menu = BaseMenu()
        menu.set_header('Actions')
        url = self.url(context='add', id='somebody')
        menu.append_new_entry("Add Contact", url)

        url = self.url(context='exportall', id='everybody')
        menu.append_new_entry("Export Contacts", url)

        url = self.url(context='importcontact', id='somebody')
        menu.append_new_entry("Import Contacts", url)
        self.layout.options_menus = dict(actions=menu)
        
        self.dispatch()

    def list_contacts(self):
        contacts = self.contacts.all()
        env = dict(contacts=contacts, letters=letters)
        template = 'trumpet:templates/consult/listcontacts.mako'
        #list_contacts.need()
        self.layout.content = self.render(template, env)
        
        
    def add_contact(self):
        user_id = self.get_current_user_id()
        schema = AddContactSchema()
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Contact Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            firstname = data['firstname']
            lastname = data.get('lastname')
            if not lastname:
                lastname = None
            email = data.get('email')
            if not email:
                email = None
            phone = data.get('phone')
            if not phone:
                phone = None
            c = self.contacts.add_user_contact(
                user_id, firstname, lastname, email, phone)
            contact = c.contact
            name = '%s %s' % (contact.firstname, contact.lastname)
            content = '<p>Contact %s added.</p>' % name
            self.layout.content = content
            return
        rendered = form.render()
        self.layout.content = rendered
        self.layout.subheader = 'Add a Contact'
            
                           
    def edit_contact(self):
        id = int(self.request.matchdict['id'])
        contact = self.contacts.get(id)
        formdata = {}
        for key in ['firstname', 'lastname', 'email', 'phone']:
            formdata[key] = getattr(contact, key)
        
        schema = AddContactSchema()
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Contact Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            firstname = data['firstname']
            lastname = data.get('lastname')
            if not lastname:
                lastname = None
            email = data.get('email')
            if not email:
                email = None
            phone = data.get('phone')
            if not phone or phone == '(000)-000-0000':
                phone = None
            kw = dict(firstname=firstname, lastname=lastname,
                      email=email, phone=phone)
            self.contacts.update(contact, **kw)
            c = self.contacts.get(id).contact
            name = '%s %s' % (c.firstname, c.lastname)
            content = '<p>Contact %s updated.</p>' % name
            self.layout.content = content
            return
        rendered = form.render(formdata)
        self.layout.content = rendered
        self.layout.subheader = 'Edit Contact %s' % id
        
        
    def delete_contact(self):
        id = self.request.matchdict['id']
        url = self.url(context='confirmdelete', id=id)
        a = '<a href="%s">Confirm Delete</a>' % url
        self.layout.content = a
        

    def confirm_delete_contact(self):
        id = self.request.matchdict['id']
        user_id = self.get_current_user_id()
        self.contacts.delete_user_contact(user_id, id)
        #self.layout.content = "Deleted"
        url = self.url(context='list', id='all')
        self.response = HTTPFound(url)
    
    def view_contact(self):
        id = self.request.matchdict['id']
        c = self.contacts.get(id)
        env = dict(c=c)
        template = 'trumpet:templates/consult/viewcontact.mako'
        self.layout.content = self.render(template, env)

    def export_contact(self):
        id = self.request.matchdict['id']
        vcf = self.contacts.export_contact(id)
        r = Response(content_type='text/vcard',
                     body=vcf.serialize())
        if c.firstname is not None:
            name = '%s_%s' % (c.firstname, c.lastname)
        else:
            name = c.lastname
        filename = '%s.vcf' % name
        r.content_disposition = 'attachment; filename="%s"' % filename
        self.response = r


    def export_all_contacts(self):
        cards = self.contacts.export_all_contacts()
        stream = ''.join((c.serialize() for c in cards))
        r = Response(content_type='text/vcard', body=stream)
        r.content_disposition = 'attachment; filename="AllContacts.vcf"'
        self.response = r

    def import_contact(self):
        env = dict()
        template = 'trumpet:templates/consult/importcontacts.mako'
        self.layout.content = self.render(template, env)
        

    def import_contact_submit(self):
        user_id = self.get_current_user_id()
        fname = self.request.POST['vcf'].filename
        ifile = self.request.POST['vcf'].file
        stream = ifile.read()
        count = 0
        excluded = []
        for card in vobject.readComponents(stream):
            cfields = parse_vcard_object(card)
            try:
                self.contacts.add_user_contact(*cfields)
                count += 1
            except IntegrityError:
                excluded.append(card)
        self.layout.content = "Imported %d cards." % count
        
        
    
        
