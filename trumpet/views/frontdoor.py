import os

from mako.template import Template

from pyramid.renderers import render
from pyramid.response import Response, FileResponse

from pyramid.path import AssetResolver

from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPFound

from pyramid.security import remember, forget
from pyramid.security import authenticated_userid

from trumpet.managers.admin.sitewebview import SiteWebviewManager
from trumpet.managers.admin.sitewebview import SiteAppManager

from trumpet.views.base import BasicView, static_asset_response
from trumpet.views.schema import LoginSchema
from trumpet.views.login import check_login_form



LOADER_TEMPLATE = """\
define(['cs!/stdlib/coffee/config', 'cs!/app/${name}'], function (config, app){
    console.log("Running ${name}");
    app();
});
"""



class FrontDoorView(BasicView):
    def __init__(self, request):
        super(FrontDoorView, self).__init__(request)
        if request.method == 'POST':
            self.handle_post()
        else:
            self.handle_get()
            
    def handle_get(self):
        request = self.request
        view = request.view_name
        subpath = request.subpath
        if not view:
            route = self.request.matched_route.name
            if route == 'home':
                self.response = HTTPFound('/frontdoor')
                return
            raise HTTPNotFound()
        elif view in ['login', 'logout']:
            # This breaks GET has no side effects
            if view == 'logout':
                return self.handle_logout({})
            self.response = HTTPFound('/frontdoor')
            return
        elif view == 'frontdoor':
            if not len(subpath):
                template = 'trumpet:templates/webview-app.mako'
                settings = self.get_app_settings()
                basecolor = settings['default.css.basecolor']
                env = dict(appname='frontdoor', basecolor=basecolor)
                content = render(template, env)
                self.response = Response(body=content)
            else:
                asset = os.path.join(
                    'haberdashery:apps/frontdoor', *subpath)
                self.response = static_asset_response(request, asset)

    def handle_login(self, post):
        if check_login_form(self.request):
            username = post['username']
            headers = remember(self.request, username)
        self.response = HTTPFound('/frontdoor')


    def handle_logout(self, post):
        headers = forget(self.request)
        if 'user' in self.request.session:
            del self.request.session['user']
        while self.request.session.keys():
            key = self.request.session.keys()[0]
            del  self.request.session[key]
        location = self.request.route_url('home')
        self.response = HTTPFound(location=location, headers=headers)
        
    

    def handle_post(self):
        request = self.request
        view = request.view_name
        subpath = request.subpath
        post = request.POST
        if view == 'login':
            return self.handle_login(post)
        elif view == 'login':
            return self.handle_logout(post)
        else:
            return self.handle_login(post)

        
    
