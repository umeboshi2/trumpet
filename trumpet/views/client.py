from pyramid.view import view_defaults

from .base import BaseViewCallable


@view_defaults(renderer='trumpet:templates/mainview.mako')
class BaseClientView(BaseViewCallable):
    def __init__(self, request):
        super(BaseClientView, self).__init__(request)
        self.settings = self.get_app_settings()
        self.data = dict()
