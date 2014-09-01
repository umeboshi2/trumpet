from pyramid.renderers import render
from pyramid.response import Response

from trumpet.views.base import BaseViewCallable

class ClientView(BaseViewCallable):
    def __init__(self, request):
        super(ClientView, self).__init__(request)
        self.get_main()

    def get_main(self):
        template = 'trumpet:templates/mainview.mako'
        settings = self.get_app_settings()
        basecolor = settings.get('default.css.basecolor', 'white-smoke')
        env = dict(appname='frontdoor', basecolor=basecolor)
        content = render(template, env)
        self.response = Response(body=content)
        self.response.encode_content()
        
    

