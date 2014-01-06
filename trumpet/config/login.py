from base import basetemplate


def configure_frontdoor(config):
    config.add_view('trumpet.views.frontdoor.FrontDoorView', name='login')
    config.add_view('trumpet.views.frontdoor.FrontDoorView', name='logout')
    config.add_view('trumpet.views.frontdoor.FrontDoorView', name='frontdoor')
    config.add_view('trumpet.views.frontdoor.FrontDoorView',
                    context='pyramid.httpexceptions.HTTPForbidden')
    #config.add_route('frontdoor', '/apps/frontdoor')
    #config.add_view('trumpet.views.webview.NodeAppView',
    #                route_name='frontdoor')
    


def configure_login(config):
    config.add_route('login', '/login')
    config.add_view('trumpet.views.login.LoginViewer',
                    route_name='login',
                    renderer=basetemplate,
                    layout='base')
    config.add_route('logout', '/logout')
    config.add_view('trumpet.views.login.LoginViewer',
                    route_name='logout',
                    renderer=basetemplate,
                    layout='base')
    # Handle HTTPForbidden errors with a
    # redirect to a login page.
    config.add_view('trumpet.views.login.LoginViewer',
                    context='pyramid.httpexceptions.HTTPForbidden',
                    renderer=basetemplate,
                    layout='base')


    ##################################
    # Views for Users
    ##################################
    route_name = 'user'
    config.add_route(route_name, '/user/{context}')
    config.add_view('trumpet.views.userview.MainViewer',
                    route_name=route_name,
                    permission='user',
                    renderer=basetemplate,
                    layout='base')
