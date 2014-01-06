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



class StaticView(BasicView):
    def __init__(self, request):
        super(StaticView, self).__init__(request)
        view = request.view_name
        if view in ['stdlib', 'stylesheets', 'components']:
            path = os.path.join(view, *request.subpath)
            asset = ':'.join(('haberdashery', path))
            self.response = static_asset_response(request, asset)
        else:
            raise HTTPNotFound()
        
        
class LoaderView(BasicView):
    def __init__(self, request):
        super(LoaderView, self).__init__(request)
        subpath = self.request.subpath
        if len(subpath) != 1:
            subpath = '/'.join(subpath)
            self.response = HTTPNotFound('no such resource')
            return
        reqname = subpath[0]
        if not reqname.endswith('.js'):
            self.response = HTTPNotFound('no such resource')
            return
        if reqname in ['cs.js', 'coffee-script.js']:
            asset = 'haberdashery:%s' % os.path.join('stdlib', reqname)
            self.response = static_asset_response(request, asset)
            return
        name = reqname[:-3]
        template = Template(LOADER_TEMPLATE)
        content = template.render(name=name)
        self.response = Response(body=content,
                                 content_type='text/javascript')
        self.response.encode_content()
        


class AppView(BasicView):
    def __init__(self, request):
        super(AppView, self).__init__(request)
        subpath = self.request.subpath
        if not len(subpath):
            raise HTTPNotFound()
        self.mgr = SiteAppManager(self.request.db)
        self.mgr.set_request(self.request)
        reqname = os.path.join(*subpath)
        if not reqname.endswith('.coffee'):
            raise HTTPNotFound()
        name = reqname[:-7]
        content = self.mgr.get_resource(name)
        r = Response(body=content, content_type='text/javascript')
        self.response = r
        self.response.encode_content()
        

class WebView(BasicView):
    def __init__(self, request):
        super(WebView, self).__init__(request)
        subpath = self.request.subpath
        if len(subpath) != 1:
            raise HTTPNotFound()
        self.mgr = SiteWebviewManager(self.request.db)
        self.mgr.set_request(self.request)
        name = subpath[0]
        webview = self.mgr.get_webview_by_name(name)
        template = 'trumpet:templates/webview-main.mako'
        env = dict(name=name)
        content = render(template, env)
        self.response = Response(body=content)
        


class NodeAppView(BasicView):
    def __init__(self, request):
        super(NodeAppView, self).__init__(request)
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

            
            
