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
    
class LoginSchema(colander.Schema):
    username = colander.SchemaNode(
        colander.String(),
        title="User Name",
    )
    password = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        widget=deform.widget.PasswordWidget(size=20),
        description="Please enter a password.")
    came_from = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=500),
        widget=deform.widget.HiddenWidget(),
        default='/',
    )


class ChangePasswordSchema(colander.Schema):
    oldpass = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        widget=deform.widget.PasswordWidget(size=20),
        description="Please enter a password.")
    newpass = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        widget=deform.widget.PasswordWidget(size=20),
        description="Please enter a password.")
    confirm = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        widget=deform.widget.PasswordWidget(size=20),
        description="Please enter a password.")


class NewUserSchema(colander.Schema):
    pass
