#!/usr/bin/env python

from pyramid.paster import get_app, setup_logging
#ini_path = '/vagrant/development.ini'
ini_path = '/vagrant/demo.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')


