import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import session_factory_from_settings

from trumpet.models.base import DBSession, Base
from trumpet.models.facebook import FB_JSON
from trumpet.models.usergroup import populate
from trumpet.models.wiki import populate_wiki
from trumpet.models.rssdata import populate_feeds
from trumpet.models.base import initialize_sql
from trumpet.models.sitecontent import populate_images, populate_sitetext
from trumpet.models.consultant import populate_ticket_status

from trumpet.config.base import basetemplate, configure_base_layout
from trumpet.config.base import configure_webviews
from trumpet.config.static import configure_static
from trumpet.config.wiki import configure_wiki
from trumpet.config.rssviewer import configure_rssviewer
from trumpet.config.login import configure_login
from trumpet.config.login import configure_frontdoor

from trumpet.config.admin import configure_admin
from trumpet.config.static import configure_sitecontent
from trumpet.config.consultant import configure_consultant

from trumpet.security import make_authn_authz_policies
from trumpet.security import authenticate


here = os.getcwd()
demo_settings = {
    'sqlalchemy.url' : 'sqlite:///%s/demo.sqlite' % here,
    }


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    settings['db.sessionmaker'] = DBSession
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    initialize_sql(engine, [populate,
                            populate_wiki,
                            populate_feeds,
                            populate_images,
                            populate_sitetext,])
    session_factory = session_factory_from_settings(settings)
    root_factory = 'trumpet.resources.RootGroupFactory'
    request_factory = 'trumpet.request.AlchemyRequest'
    # setup authn and authz
    appname = 'demo'
    secret = settings['%s.authn.secret' % appname]
    cookie = settings['%s.authn.cookie' % appname]
    timeout = int(settings['%s.authn.timeout' % appname])
    authn_policy, authz_policy = make_authn_authz_policies(
        secret, cookie, callback=authenticate,
        timeout=timeout, tkt=False)

    config = Configurator(settings=settings,
                          root_factory=root_factory,
                          request_factory=request_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy,
                          session_factory=session_factory
                          )
    config.include('cornice')
    configure_frontdoor(config)
    configure_static(config)
    configure_base_layout(config)
    
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_view('trumpet.views.frontdoor.FrontDoorView',
                    route_name='home',)

    #configure_login(config)
    #configure_rssviewer(config, '/rssviewer')
    #configure_wiki(config, '/wiki')
    #configure_admin(config)
    #configure_sitecontent(config)
    #configure_consultant(config)
    config.scan('trumpet.views.rest.users')
    config.scan('trumpet.views.rest.webview')
    config.scan('trumpet.views.rest.sitecontent')
    config.scan('trumpet.views.rest.simplerss')


    configure_webviews(config)
    
    return config.make_wsgi_app()

