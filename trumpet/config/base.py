

def configure_base_views(config):
    # bower components
    config.add_view('trumpet.views.base.StaticView', name='components')
    # css 
    config.add_view('trumpet.views.base.StaticView', name='css')
    # fonts
    config.add_view('trumpet.views.base.StaticView', name='fonts')
    # local libs
    config.add_view('trumpet.views.base.StaticView', name='lib')
    # applications
    config.add_view('trumpet.views.appview.AppView', name='app')

    # this is for pulling binaries from a database or filesystem
    rootpath = 'blobs'
    config.add_route('blob', '%s/{filetype}/{id}' % rootpath)
    config.add_view('trumpet.views.blobs.BlobViewer', route_name='blob',
                    renderer='string',)
    
    # these are for apps stored in the database
    #config.add_view('trumpet.views.webview.LoaderView', name='loader')
    #config.add_view('trumpet.views.webview.AppView', name='app')
    #config.add_view('trumpet.views.webview.WebView', name='webview')

    
    



def configure_trumpet_cases(config, rootpath='mslcases',
                            permission='consultant'):
    route_name = 'msl_casesjson'
    config.add_route(route_name,
                     '/%s/casesjson/{context}/{id}' % rootpath)
    config.add_view('trumpet.views.cases.CaseJSONViewer',
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    route_name = 'msl_casesfrag'
    config.add_route(route_name,
                     '/msl/casesfrag/{context}/{id}')
    config.add_view('trumpet.views.cases.CaseFrag',
                    route_name=route_name,
                    renderer='string',
                    layout='base',
                    permission=permission)



def configure_consultant(config, rootpath='/consult', permission='consultant'):
    route_name = 'consult_json'
    config.add_route(route_name,
                     '%s/json/{context}/{id}' % rootpath)
    config.add_view('trumpet.views.consultant.json.JSONViewer',
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    print "ADDED JSONViewer"
    route_name = 'consult_frag'
    config.add_route(route_name,
                     '%s/frag/{context}/{id}' % rootpath)
    config.add_view('trumpet.views.consultant.frag.FragViewer',
                    route_name=route_name,
                    renderer='string',
                    layout='base',
                    permission=permission)
    
    route_name = 'consult_caljson'
    config.add_route(route_name,
                     '%s/caljson/{context}/{id}' % rootpath)
    config.add_view('trumpet.views.consultant.calendar.CalendarJSONViewer',
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    

    
