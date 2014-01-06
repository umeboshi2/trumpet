import colander
import deform

from trumpet.resources import MemoryTmpStore

tmpstore = MemoryTmpStore()

def deferred_choices(node, kw):
    choices = kw['choices']
    return deform.widget.SelectWidget(values=choices)

def make_select_widget(choices):
    return deform.widget.SelectWidget(values=choices)


class AddUserSchema(colander.Schema):
    user = colander.SchemaNode(
        colander.Integer(),
        title="User",
        widget=deferred_choices,
        description="User to add",
        )
    
    
class NameSelectSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.Integer(),
        title="Name",
        widget=deferred_choices,
        )
    
class UploadFileSchema(colander.Schema):
    upload = colander.SchemaNode(
        deform.FileData(),
        widget=deform.widget.FileUploadWidget(tmpstore),
        )
    
