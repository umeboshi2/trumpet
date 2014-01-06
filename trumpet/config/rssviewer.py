from base import basetemplate
from base import add_view


def configure_rssviewer(config, rootpath, permission='manage'):
    config.add_route('rssviewer', '%s/{context}/{feed}' % rootpath)
    add_view(config, 'trumpet.views.rssviewer.MainViewer',
             'rssviewer', permission=permission)
