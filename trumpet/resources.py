from pyramid.security import Allow, Everyone, Authenticated


class Resource(dict):
    def __init__(self, name, parent):
        self.__name__ = name
        self.__parent__ = parent
    
# the acl entries are allow/deny, group, permission
class RootGroupFactory(Resource):
    __default_acl__ = [
        (Allow, Everyone, 'public'),
        (Allow, Authenticated, 'user'),
        (Allow, 'manager', 'manage'),
        (Allow, 'admin', ('admin', 'manage')),
        (Allow, 'manager', ('wiki_add', 'wiki_edit')),
        (Allow, 'admin', ('wiki_add', 'wiki_edit')),
        (Allow, 'manager', 'consultant'),
        (Allow, 'admin', 'consultant'),
        ]
    authn_policy = None

    @property
    def __acl__(self):
        return self.__default_acl__
    

    def add_resource(self, name, orm_class):
        self[name] = ORMContainer(name, self, self.request, orm_class)

    def __init__(self, request):
        self.request = request
        #self['admin'] = dict()
    

# straight from deform docs
class MemoryTmpStore(dict):
    def preview_url(self, name):
        return None
