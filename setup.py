from setuptools import setup, find_packages
import sys
import os

version = '0.2.0'

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'docutils',        # only needed for wiki
    'pyramid-beaker',  # session management

    # we need to think about using another
    # postgresql/sqlalchemy package that
    # can be used with pypy
    'psycopg2',        # dbapi for postgresql
    
    # we need to stop using deform
    'pyramid-deform',  # we will start using deform/colander/peppercorn
    'deform',

    # this is for the simple rss viewer example
    'feedparser',      # only needed for rssviewer

    
    'Pillow',          # image management
    'vobject',         # vcard, iCal support
    'icalendar',       # more iCal support

    'waitress',

    
    #'twill',
    #'mechanize',       # mechanize may be better than twill sometimes
    #'beautifulsoup4',
    #'lxml',            # lxml parser for beautifulsoup4
    #'facebook-sdk',
    #'filemagic',       # useful for identifying blobs
    #'markdown',

    
    'pyramid-mako',
    'cornice',         # REST views
    'haberdashery>=0.0dev',
    
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
      [console_scripts]
      trumpet-make-tmpl-links = trumpet.scripts.Make_tmpl_links:main
      """,
      )
