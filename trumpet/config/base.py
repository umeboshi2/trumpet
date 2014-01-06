basetemplate = 'trumpet:templates/base.mako'

def configure_base_layout(config):
    config.include('pyramid_layout')
    baselayout = 'trumpet.layouts.BaseLayout'
    template = 'trumpet:templates/layouts/base.mako'
    config.add_layout(baselayout, template, name='base')

def configure_mobile_layout(config):
    config.include('pyramid_layout')
    layout = 'trumpet.layouts.MobileLayout'
    template = 'trumpet:templates/layouts/mobile.mako'
    config.add_layout(layout, template, name='mobile')
    

def add_view(config, view, route_name, **kw):
    config.add_view(view, route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    **kw)


def configure_webviews(config):
    #view = 'trumpet.views.webview.StdLibView'
    #config.add_route('stdlib', '/stdlib/*subpath')
    #config.add_view(view, route_name='stdlib')

    config.add_view('trumpet.views.webview.StaticView', name='stdlib')
    config.add_view('trumpet.views.webview.StaticView', name='stylesheets')
    config.add_view('trumpet.views.webview.StaticView', name='components')
    

    config.add_view('trumpet.views.webview.LoaderView', name='loader')
    config.add_view('trumpet.views.webview.AppView', name='app')

    config.add_view('trumpet.views.webview.NodeAppView', name='apps')
    
    
    config.add_view('trumpet.views.webview.WebView', name='webview')

    
