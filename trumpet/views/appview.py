import os

from mako.template import Template

from pyramid.renderers import render
from pyramid.response import Response, FileResponse

from pyramid.path import AssetResolver

from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPFound


from trumpet.managers.admin.sitewebview import SiteWebviewManager
from trumpet.managers.admin.sitewebview import SiteAppManager

from trumpet.views.base import BasicView, static_asset_response



LOADER_TEMPLATE = """\
define(['cs!/stdlib/coffee/config', 'cs!/app/${name}'], function (config, app){
    console.log("Running ${name}");
    app();
});
"""



class AppView(BasicView):
    def __init__(self, request):
        super(AppView, self).__init__(request)
        view = request.view_name
        subpath = request.subpath
        if not len(subpath):
            raise HTTPNotFound()
        appname = subpath[0]
        if len(subpath) == 1:
            # check for existence
            asset = 'haberdashery:apps/%s' % appname
            resolver = AssetResolver()
            descriptor = resolver.resolve(asset)
            if not descriptor.exists():
                raise HTTPNotFound()
            # send back index to start load app
            settings = self.get_app_settings()
            basecolor = settings['default.css.basecolor']
            template = 'trumpet:templates/webview-app.mako'
            env = dict(appname=appname, basecolor=basecolor)
            content = render(template, env)
            self.response = Response(body=content)
        else:
            #asset = 'haberdashery:apps/%s' % appname
            asset = os.path.join('haberdashery:apps', *subpath)
            self.response = static_asset_response(request, asset)

            
            
