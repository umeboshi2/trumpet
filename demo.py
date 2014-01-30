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

from trumpet.config.base import configure_base_views
from trumpet.config.login import configure_frontdoor

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
    configure_base_views(config)
    configure_frontdoor(config)
    
    config.add_route('home', '/')
    config.add_view('trumpet.views.frontdoor.FrontDoorView',
                    route_name='home',)

    config.scan('trumpet.views.rest.base')
    config.scan('trumpet.views.rest.users')
    config.scan('trumpet.views.rest.webview')
    config.scan('trumpet.views.rest.sitecontent')
    config.scan('trumpet.views.rest.simplerss')


    
    return config.make_wsgi_app()

