import colander


class AddUserSchema(colander.Schema):
    user = colander.SchemaNode(
        colander.Integer(),
        title="User",
        description="User to add",
    )


class NameSelectSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.Integer(),
        title="Name",
    )


# FIXME upload files in post request
#from trumpet.resources import MemoryTmpStore
#tmpstore = MemoryTmpStore()
# class UploadFileSchema(colander.Schema):
#    upload = colander.SchemaNode(
#        deform.FileData(),
#        widget=deform.widget.FileUploadWidget(tmpstore),
#        )

class LoginSchema(colander.Schema):
    username = colander.SchemaNode(
        colander.String(),
        title="User Name",
    )
    password = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        description="Please enter a password.")
    came_from = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=500),
        default='/',
    )


class ChangePasswordSchema(colander.Schema):
    oldpass = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        description="Please enter a password.")
    newpass = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        description="Please enter a password.")
    confirm = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=5, max=100),
        description="Please enter a password.")


class NewUserSchema(colander.Schema):
    pass
