from pyramid.view import view_defaults
from pyramid.renderers import render
from pyramid.response import Response

from trumpet.views.base import BaseViewCallable


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

    def _make_response(self, settings, appname):
        content = make_app_page(appname, settings,
                                request=self.request)
        self.response = Response(body=content)
        self.response.encode_content()

    def _make_env(self, appname):
        env = dict(appname=appname,
                   basecolor=basecolor,
                   csspath=csspath,
                   jspath=jspath)
        return env

    #@view_config(route_name='home')
    # def index(self):
    #    self.data['appname'] = self.settings.get('default.js.mainapp', 'index')
    #    return self.data
