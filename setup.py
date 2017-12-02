from setuptools import setup, find_packages
import sys
import os

# http://stackoverflow.com/a/22147112/1869821
# if you are not using vagrant, just delete os.link directly,
# The hard link only saves a little disk space, so you should not care
if os.environ.get('USER','') == 'vagrant':
    del os.link

version = '0.2.0'


requires = [
    'chert', 
    'pyramid',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'pyramid-beaker',  # session management
    'pyramid-mako',
    'cornice',         # REST views
    'waitress',
    # we need to think about using another
    # postgresql/sqlalchemy package that
    # can be used with pypy
    'psycopg2',        # dbapi for postgresql
    'requests',
    # testing below
    #'versiontools',
]

setup(name='trumpet',
      version=version,
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
      applet=trumpet.scaffolds:TrumpetAppletTemplate
      [console_scripts]
      trumpet-make-tmpl-links = trumpet.scripts.Make_tmpl_links:main
      """,
      dependency_links=[
          'git+https://github.com/umeboshi2/chert.git#egg=chert'
      ],
      )
