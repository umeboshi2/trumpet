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


class AppView(BasicView):
    def __init__(self, request):
        super(AppView, self).__init__(request)
        assetpath = 'trumpet:static/apps'
        view = request.view_name
        subpath = request.subpath
        if not len(subpath):
            raise HTTPNotFound()
        appname = subpath[0]
        if len(subpath) == 1:
            # check for existence
            asset = '%s/%s' % (assetpath, appname)
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
            self.response.encode_content()
        else:
            #asset = 'haberdashery:apps/%s' % appname
            asset = os.path.join(assetpath, *subpath)
            self.response = static_asset_response(request, asset)

            
            
class AdminAppView(BasicView):
    def __init__(self, request):
        super(AdminAppView, self).__init__(request)
        assetpath = 'trumpet:static/apps/admin'
        view = request.view_name
        subpath = request.subpath
        if not len(subpath):
            #raise HTTPNotFound()
            #self.response = Response(body='admin page')
            self.response = HTTPFound('/admin/main')
            return
        appname = subpath[0]
        if len(subpath) == 1:
            # check for existence
            asset = '%s/%s' % (assetpath, appname)
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
            self.response.encode_content()
        else:
            asset = os.path.join(assetpath, *subpath)
            self.response = static_asset_response(request, asset)

            
            
