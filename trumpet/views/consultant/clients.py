import colander
import deform

from trumpet.views.menus import BaseMenu

from trumpet.views.base import prepare_layout
from trumpet.views.base import BaseViewer


from trumpet.managers.consultant.clients import ClientManager
from trumpet.managers.consultant.contacts import ContactManager

from trumpet.views.consultant.base import prepare_base_layout
from trumpet.views.schema import deferred_choices, make_select_widget


class AddClientSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        title='Name',
        )
    contact = colander.SchemaNode(
        colander.Integer(),
        title='Contact',
        widget=deferred_choices,
        )
    address = colander.SchemaNode(
        colander.String(),
        title='Address',
        widget=deform.widget.TextAreaWidget(rows=4, cols=30),
        missing=colander.null,
        )
    description = colander.SchemaNode(
        colander.String(),
        title='Description',
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        missing=colander.null,
        )

def prepare_main_layout(request):
    prepare_base_layout(request)
    layout = request.layout_manager.layout
    layout.title = 'Consultant Clients'
    layout.header = 'Consultant Clients'
    layout.subheader = 'Clients Area'
    

    

class ClientViewer(BaseViewer):
    def __init__(self, request):
        BaseViewer.__init__(self, request)
        prepare_main_layout(self.request)
        self.clients = ClientManager(self.request.db)
        self.contacts = ContactManager(self.request.db)
        self._dispatch_table = dict(
            list=self.list_clients,
            add=self.add_client,
            delete=self.delete_client,
            confirmdelete=self.confirm_delete_client,
            editclient=self.edit_client,
            viewclient=self.view_client,)
        self.context = self.request.matchdict['context']
        self._view = self.context

        menu = BaseMenu()
        menu.set_header('Actions')
        url = self.url(context='add', id='somebody')
        menu.append_new_entry("Add Client", url)
        self.layout.options_menus = dict(actions=menu)
        
        self.dispatch()

    def list_clients(self):
        clients = self.clients.all()
        env = dict(clients=clients)
        template = 'trumpet:templates/consult/listclients.mako'
        self.layout.content = self.render(template, env)
        
    def _make_form(self):
        schema = AddClientSchema()
        clist = self.contacts.all()
        choices = [(c.id, '%s %s' % (c.firstname, c.lastname)) for c in  clist]
        schema['contact'].widget = make_select_widget(choices)
        form = deform.Form(schema, buttons=('submit',))
        self.layout.resources.deform_auto_need(form)
        return schema, form
    
    def add_client(self):
        schema, form = self._make_form()
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Client Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            name = data['name']
            contact_id = int(data['contact'])
            address = data['address']
            description = data['description']
            c = self.clients.add(name, contact_id, address, description)
            content = '<p>Client %s added.</p>' % c.name
            self.layout.content = content
            return
        rendered = form.render()
        self.layout.content = rendered
        self.layout.subheader = 'Add a Client'
            
                           
    def edit_client(self):
        id = int(self.request.matchdict['id'])
        client = self.clients.get(id)
        formdata = {}
        for key in ['name', 'address', 'description']:
            formdata[key] = getattr(client, key)
        formdata['contact'] = client.contact_id
        schema, form = self._make_form()
        if 'submit' in self.request.POST:
            controls = self.request.POST.items()
            self.layout.subheader = 'Client Submitted'
            try:
                data = form.validate(controls)
            except deform.ValidationFailure, e:
                self.layout.content = e.render()
                return
            self.clients.update(client, **dict(controls))
            client = self.clients.get(id)
            content = '<p>Client %s updated.</p>' % client.name
            self.layout.content = content
            return
        rendered = form.render(formdata)
        self.layout.content = rendered
        self.layout.subheader = 'Edit Client %s' % client.name
        
    def delete_client(self):
        pass

    def confirm_delete_client(self):
        pass
    
    def view_client(self):
        self.layout.content = "what are we doing?"
        
