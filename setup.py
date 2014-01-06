from setuptools import setup, find_packages
import sys
import os

version = '0.1.1'

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'docutils',        # only needed for wiki
    'feedparser',      # only needed for rssviewer
    'pyramid-beaker',  # session management
    'pyramid-deform',  # we will start using deform/colander/peppercorn
    'deform',
    'Mako',            # we have mako templates for forms
    'FormEncode',      # we use parts of formencode to make html
    'Pillow',          # image management
    'vobject',         # vcard, iCal support
    'icalendar',       # more iCal support
    'haberdashery>=0.0dev',
    'waitress',
    'twill',
    'mechanize',       # mechanize may be better than twill sometimes
    'beautifulsoup4',
    'lxml',            # lxml parser for beautifulsoup4
    'facebook-sdk',
    'psycopg2',        # dbapi for postgresql
    'filemagic',       # useful for identifying blobs
    'markdown',
    'pyramid-layout',
    'cornice',         # REST views
    
]

setup(name='trumpet',
      version=version,
      setup_requires=[],
      description="build a website with pyramid",
      long_description="""\
Start a website with pyramid""",
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='pyramid, sqlalchemy, scss',
      author='Joseph Rawson',
      author_email='joseph.rawson.works@gmail.com',
      url='https://github.com/umeboshi2/trumpet',
      license='Public Domain',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      # -*- Entry points: -*-
      [pyramid.scaffold]
      trumpet=trumpet.scaffolds:TrumpetProjectTemplate
      # A console script to serve the application and monitor static resources
      [console_scripts]
      trumpet-make-tmpl-links = trumpet.scripts.Make_tmpl_links:main
      """,
      dependency_links=[
      'https://github.com/umeboshi2/haberdashery/archive/master.tar.gz#egg=haberdashery-0.0dev',
      ],
      )
