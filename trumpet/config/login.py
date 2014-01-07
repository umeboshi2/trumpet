
def configure_frontdoor(config):
    config.add_view('trumpet.views.frontdoor.FrontDoorView', name='login')
    config.add_view('trumpet.views.frontdoor.FrontDoorView', name='logout')
    config.add_view('trumpet.views.frontdoor.FrontDoorView', name='frontdoor')
    config.add_view('trumpet.views.frontdoor.FrontDoorView',
                    context='pyramid.httpexceptions.HTTPForbidden')


