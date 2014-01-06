# I'm not sure if keyword parameters are appropriate


def configure_deform(config, name='deform_static'):
    config.add_static_view(name, 'deform:static')


def configure_trumpet(config, name='trumpet_static'):
    config.add_static_view(name, 'trumpet:static')


def configure_static(config, deform='deform_static',
                     trumpet='trumpet_static'):
    configure_deform(config, name=deform)
    configure_trumpet(config, name=trumpet)


def configure_sitecontent(config, rootpath='/blob'):
    config.add_route('blob', '%s/{filetype}/{id}' % rootpath)
    config.add_view('trumpet.views.blobs.BlobViewer', route_name='blob',
                    renderer='string',)
                    
    
