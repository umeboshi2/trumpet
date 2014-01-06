from base import basetemplate
from base import add_view

main_view = 'trumpet.views.admin.main.MainViewer'


def configure_admin(config, rootpath='/admin', permission='admin'):
    config.add_route('admin', rootpath)
    add_view(config, main_view, 'admin')
    config.add_route('admin_images', '%s/images/{context}/{id}' % rootpath)
    add_view(config, 'trumpet.views.admin.images.ImageManagementViewer',
             'admin_images', permission=permission)
    config.add_route('admin_sitetext', '%s/sitetext/{context}/{id}' % rootpath)
    add_view(config, 'trumpet.views.admin.sitetext.SiteTextViewer',
             'admin_sitetext', permission=permission)
    config.add_route('admin_users', '%s/users/{context}/{id}' % rootpath)
    add_view(config, 'trumpet.views.admin.users.UserManagementViewer',
               'admin_users', permission=permission)

    config.add_route('admin_users_bb', '%s/usersbb' % rootpath)
    add_view(config, 'trumpet.views.admin.usersbb.AppViewer',
               'admin_users_bb', permission=permission)

    route = 'admin_sitecontent_mgr'
    config.add_route(route, '%s/sitecontentmgr/{context}/{id}' % rootpath)
    add_view(config, 'trumpet.views.admin.contentmgr.MainViewer',
             route, permission=permission)

    route = 'admin_sitecontent_mgr_bb'
    config.add_route(route, '%s/sitecontentmgrbb/{context}/{id}' % rootpath)
    add_view(config, 'trumpet.views.admin.contentmgrbb.AppViewer',
             route, permission=permission)


    route = 'admin_webviews'
    config.add_route(route, '%s/webviewmgr/{context}/{id}' % rootpath)
    add_view(config, 'trumpet.views.admin.webviewmgr.MainViewer',
             route, permission=permission)
