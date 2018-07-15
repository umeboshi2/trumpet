

from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.path import AssetResolver


def static_asset_response(request, asset):
    resolver = AssetResolver()
    descriptor = resolver.resolve(asset)
    if not descriptor.exists():
        raise HTTPNotFound(request.url)
    path = descriptor.abspath()
    response = FileResponse(path, request)
    zip_response = False
    for ending in ['.css', '.js', '.coffee', '.html', '.ttf']:
        if path.endswith(ending):
            zip_response = True
    if zip_response:
        response.encode_content()
    for ending in ['.css', '.js']:
        # one day for css and js
        if path.endswith(ending):
            response.cache_expires(3600 * 24)
            response.cache_control.public = True
    if path.endswith('.ttf'):
        # one year for fonts
        response.cache_expires(3600 * 24 * 365)
        response.cache_control.public = True
    return response


class BaseView(object):
    def __init__(self, request):
        self.request = request

    def get_app_settings(self):
        return self.request.registry.settings


class BaseUserView(BaseView):
    def get_current_user(self):
        "Get user db object"
        return self.request.user


class BaseViewCallable(BaseView):
    def __init__(self, request):
        super(BaseViewCallable, self).__init__(request)
        self.response = None
        self.data = {}

    def __call__(self):
        if self.response is not None:
            return self.response
        else:
            return self.data


class BaseUserViewCallable(BaseViewCallable, BaseUserView):
    pass


class BaseResource(BaseViewCallable):
    def __init__(self, request, context=None):
        super(BaseResource, self).__init__(request)
        if not hasattr(self, 'dbmodel'):
            msg = "need to set dbmodel property before __init__"
            raise RuntimeError(msg)

    def _query(self):
        return self.db.query(self.dbmodel)

    def _get(self, id):
        return self._query().get(id)

    def get(self):
        id = int(self.request.matchdict['id'])
        return self._get(id).serialize()


class BaseManagementResource(BaseResource):
    def __init__(self, request, context=None):
        super(BaseManagementResource, self).__init__(request)
        if not hasattr(self, 'mgrclass'):
            msg = "need to set mgrclass property before __init__"
            raise RuntimeError(msg)
        self.mgr = self.mgrclass(self.request.dbsession)
        
    def get(self):
        id = int(self.request.matchdict['id'])
        return self.mgr.get(id).serialize()
    
    def collection_get(self):
        # FIXME: use offset, limit, and pass filters
        objects = self.mgr.all()
        return dict(data=[o.serialize() for o in objects])
        
        
