from pyramid.view import view_defaults

from .base import BaseViewCallable


@view_defaults(renderer='trumpet:templates/mainview.mako')
class BaseClientView(BaseViewCallable):
    def __init__(self, request):
        super(BaseClientView, self).__init__(request)
        self.settings = self.get_app_settings()
        self.data = dict(
            basecolor=self.settings.get('default.css.basecolor', 'vanilla'),
            csspath=self.settings.get(
                'default.css.path', '/assets/stylesheets'),
            jspath=self.settings.get('default.js.path', '/assets/client'),)

    # @view_config(route_name='home')
    # def index(self):
    #    option = 'default.js.mainapp'
    #    self.data['appname'] = self.settings.get(option, 'index')
    #    return self.data
