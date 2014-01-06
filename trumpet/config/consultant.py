from base import basetemplate
from base import add_view

viewers = dict(contacts='ContactViewer',
               clients='ClientViewer',
               calendar='CalendarViewer',
               tickets='TicketViewer')












def configure_trumpet_cases(config, rootpath='mslcases',
                            permission='consultant'):
    route_name = 'msl_cases'
    config.add_route(route_name,
                     '/%s/cases/{context}/{id}' % rootpath)
    #FIXME: better module name
    config.add_view('trumpet.views.cases.MainCaseViewer',
                    route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)
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


def configure_trumpet_docs(config, rootpath='msldocs',
                            permission='consultant'):
    route_name = 'msl_docs'
    config.add_route(route_name,
                     '/%s/docs/{context}/{id}' % rootpath)
    #FIXME: better module name
    config.add_view('trumpet.views.documents.MainDocumentViewer',
                    route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)











def configure_consultant(config, rootpath='/consult', permission='consultant'):
    config.add_route('consult', rootpath)
    config.add_view('trumpet.views.consultant.main.MainViewer',
                    route_name='consult',
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)
    for route in ['contacts', 'clients', 'calendar', 'tickets']:
        route_name = 'consult_%s' % route
        config.add_route(route_name,
                         '%s/%s/{context}/{id}' % (rootpath, route))
        view = 'trumpet.views.consultant.%s.%s' % (route, viewers[route])
        print "ADDVIEW", view
        config.add_view(view, route_name=route_name,
                        renderer=basetemplate,
                        layout='base',
                        permission=permission)
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
    

    
    return
    

        ###################################
    route_name = 'consult_tickets'
    config.add_route(route_name,
                     '/consult/tickets/{context}/{id}')
    #FIXME: better module name
    config.add_view('trumpet.views.tickets.MSLViewer',
                    route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)
    route_name = 'consult_tktjson'
    config.add_route(route_name,
                     '/consult/tktjson/{context}/{id}')
    config.add_view('trumpet.views.tickets.TicketJSONViewer',
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    route_name = 'consult_tktfrag'
    config.add_route(route_name,
                     '/consult/tktfrag/{context}/{id}')
    config.add_view('trumpet.views.tickets.TicketFrag',
                    route_name=route_name,
                    renderer='string',
                    layout='base',
                    permission=permission)
    route_name = 'consult_phonecalls'
    config.add_route(route_name,
                     '/consult/phonecalls/{context}/{id}')
    config.add_view('trumpet.views.phonecalls.MSLPhoneViewer',
                    route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)
    route_name = 'consult_pcallfrag'
    config.add_route(route_name,
                     '/consult/pcallfrag/{context}/{id}')
    config.add_view('trumpet.views.phonecalls.PhoneCallFrag',
                    route_name=route_name,
                    renderer='string',
                    layout='base',
                    permission=permission)
    route_name = 'msl_pcalljson'
    config.add_route(route_name,
                     '/consult/pcalljson/{context}/{id}')
    config.add_view('trumpet.views.phonecalls.PhoneCallJSONViewer',
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    
    
    route_name = 'consult_scandocs'
    config.add_route(route_name,
                     '/consult/scandocs/{context}/{id}')
    config.add_view('trumpet.views.consultant.pdfscans.ScannedDocumentsViewer',
                    route_name=route_name,
                    renderer=basetemplate,
                    layout='base',
                    permission=permission)

    route_name = 'consult_scandoc_json'
    config.add_route(route_name,
                     '/consult/scandocsjson/{context}/{id}')
    view = 'trumpet.views.consultant.pdfscans.ScannedDocumentsJSONViewer'
    config.add_view(view,
                    route_name=route_name,
                    renderer='json',
                    layout='base',
                    permission=permission)
    
