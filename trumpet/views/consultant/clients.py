import colander
import deform



from trumpet.managers.consultant.clients import ClientManager
from trumpet.managers.consultant.contacts import ContactManager

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

