import os
import time
import cPickle as Pickle
from urlparse import urlparse, parse_qs
from ConfigParser import ConfigParser

from twill import get_browser

# IMPORTANT
# =========
# I made this module for a website running
# on my raspberrypi.  This allows you to
# use your web service as a "desktop"
# application, relieving the user of the
# need to be hosted on a resolvable domain.
# This module should NEVER be used on
# a live multiuser application, as this module
# depends on having the facebook user PASSWORD.

plumdir = os.path.expanduser('~/Private/config/plum')
config_filename = os.path.join(plumdir, 'plumrc')
cookiejar = os.path.join(plumdir, 'cookiejar')

config = ConfigParser()
config.read([config_filename])

# app info
app_id = config.get('fbapp', 'app_id')
app_secret = config.get('fbapp', 'app_secret')
fb_redirect = config.get('fbapp', 'fb_redirect')
cookie_accepted = config.get('fbapp', 'cookie_accepted')
fb_oauth_dialog = config.get('fbapp', 'fb_oauth_dialog')
fb_graph_token = config.get('fbapp', 'fb_graph_token')
ss_redirect_uri = config.get('fbapp', 'ss_redirect_uri')
fb_query = 'client_id=%s&redirect_uri=%s&respone_type=token' \
    % (app_id, ss_redirect_uri)
ss_query_prefix = 'client_id=%s&redirect_uri=%s&client_secret=%s&code=' \
    % (app_id, ss_redirect_uri, app_secret)

# account info
email = config.get('fbauth', 'email')
password = config.get('fbauth', 'password')


def make_login_url(scope=[]):
    query = fb_query
    if scope:
        scope = ','.join(scope)
        query = '%s&%s' % (fb_query, scope)
    url = '%s?%s' % (fb_oauth_dialog, query)
    return url

def _parse_frag(fragment):
    data = parse_qs(fragment)
    token = data['access_token'][0]
    expires = int(data['expires'][0])
    return token, expires

def _get_code(parsed):
    return parse_qs(parsed.query)['code'][0]


def _enter_login_form(browser, email, password):
    form = browser.get_all_forms()[0]
    form.set_value(email, 'email')
    form.set_value(password, 'pass')
    browser.submit('login')
    parsed = urlparse(browser.get_url())
    browser.save_cookies(cookiejar)
    return parsed

def _prelogin_fb(browser, url):
    browser.go(url)
    location = browser.get_url()
    parsed = urlparse(location)
    if not parsed.path.startswith(cookie_accepted):
        parsed = _enter_login_form(browser, email, password)
    return _get_code(parsed)

def _exchange_code_for_token(browser, code):
    query = ss_query_prefix + code
    url = '%s?%s' % (fb_graph_token, query)
    browser.go(url)


def login_to_facebook(browser, scope=[]):
    url = make_login_url(scope=scope)
    code = _prelogin_fb(browser, url)
    _exchange_code_for_token(browser, code)
    token, expires = _parse_frag(browser.get_html())
    return token, expires


def get_access_token():
    pickled_token = os.path.expanduser('~/Private/config/plum/token.pickle')
    if os.path.isfile(pickled_token):
        token, expires = Pickle.load(file(pickled_token))
        if expires > time.time():
            return token
    b = get_browser()
    b.set_agent_string('Mozilla 5.0')
    if os.path.exists(cookiejar):
        b.load_cookies(cookiejar)
    token, expires = login_to_facebook(b)
    expires = time.time() + expires
    pt = file(pickled_token, 'w')
    Pickle.dump((token, expires), pt)
    return token


   

if __name__ == '__main__':
    from twill import get_browser
    b = get_browser()
    b.set_agent_string('Mozilla 5.0')
    if os.path.exists(cookiejar):
        b.load_cookies(cookiejar)
    token, expires = login_to_facebook(b)
    

