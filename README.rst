=======
trumpet
=======


.. image:: https://img.shields.io/pypi/v/trumpet.svg
        :target: https://pypi.python.org/pypi/trumpet

.. image:: https://img.shields.io/travis/umeboshi2/trumpet.svg
        :target: https://travis-ci.org/umeboshi2/trumpet

.. image:: https://readthedocs.org/projects/trumpet/badge/?version=latest
        :target: https://trumpet.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/umeboshi2/trumpet/shield.svg
     :target: https://pyup.io/repos/github/umeboshi2/trumpet/
     :alt: Updates


Build a website with pyramid


* Free software: UNLICENSED
* Documentation: https://trumpet.readthedocs.io.



Getting Started
---------------

- Change directory into your newly created project.

    cd trumpet

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Configure the database.

    env/bin/initialize_trumpet_db development.ini

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini


Abstract
----------

Trumpet uses the `Pyramid`_ framework to provide services to help
build websites.  The goal of this project is to provide a more opinionated
framework that focuses on `REST`_ resources and provides a system to
develop `Single Page Applications`_, as well as use some simple ones
provided by the trumpet package.

A page on the static resources used to build SPA's can be found `here`_.

.. _`Pyramid`: http://www.pylonsproject.org/
.. _`REST`: http://en.wikipedia.org/wiki/Representational_state_transfer
.. _`Single Page Applications`: http://en.wikipedia.org/wiki/Single-page_application
.. _`here`: https://github.com/umeboshi2/trumpet/blob/master/docs/TrumpetStaticResources.md


NEWS
-----

Trumpet is being converted into it's original concept of being a 
set of building blocks to help build a pyramid web service.  In the past, 
a large amount of time has been spent on managing static resources 
through pyramid and python.  A separate project, haberdashery, was created 
to help manage the static resources in a python package.  While the idea 
of developing the static resources has evolved into an environment where 
no python is required, except for a few development scripts, many of the 
ideas used previously have been made obsolescent by using nodejs and 
compass.

Trumpet is now focused primarily on providing server side components to 
help make a website/application.  Static resources are to be developed 
in another project, although they may be served through the pyramid 
server.

Goals
------

* user management

  - login/logout
  - administer users via REST
  - reflective sqlalchemy code, db should provide minimum user/password tables

* db support

  - common sqlalchemy code for all databases
  - request object with attached sessionmaker

* session management

  - minimal use of cookies
  - use access_token as parameter to all requests requiring authentication
  - policies for session management

    + sessions per user (configure number of sessions a user can have)
    + sessions per device (register devices to user?)
    + session duration
    + session timeout/expiration
  
  - is beaker good enough?
    
* view classes
  
  - basic view classes to be used by all views
    
    + common methods
    + app settings available
      
  - base user aware view class
    
    - base class for requests that need auth
      
  - base cornice resource
  - base static resource
  - base page resource
    
    - send the html page that runs the app
    - use template to fill the head with links and meta info
    - handle permissions for access to app
      
- server side validation
  
  - use colander to build schemas for validation
    
- integrate with job servers for long running jobs

  
Old
-----

Remnants of the old README can be found [here](https://github.com/umeboshi2/trumpet/blob/master/docs/misc.md).

Features
--------

* TODO

  - remember vobject and icalendar to make .vcf files, etc...





Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

