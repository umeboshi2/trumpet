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



News
-----

Trumpet is getting a bit closer to the original intended goal of
being a set of building blocks and tools to help build a pyramid
web application.  Management of static resources has moved
completely away from python.  Compass is still being used to
help manage the stylesheets.  Webpack is being used to handle the
javascript, as well as some css, fonts, etc. Currently, cookiecutter
is being used to test generating project skeletons, replacing the
previous scaffold.

The general concept is to have support for creating web applications
with different hosting requirements.  A creative use of cookiecutter
templates may provide the ability to generate a pyramid site, a static
application/site, or even a tree of static assets that can be used in
many projects.


Goals and Progress
---------------------

* user management

  - login/logout
  - administer users via REST
  - reflective sqlalchemy code, db should provide minimum user/password tables

* db support

  - common sqlalchemy code for all databases **complete**
  - request object with attached sessionmaker **completed by upstream scaffold**

* session management **obsolete?**

  - minimal use of cookies **completed by using JSON Web Tokens**
  - use access_token as parameter to all requests requiring authentication
  - policies for session management *now token policies*
    
    + sessions per user (configure number of sessions a user can have)
    + sessions per device (register devices to user?)
    + session duration
    + session timeout/expiration
  
* view classes
  
  - basic view classes to be used by all views
    
    + common methods *WIP*
    + app settings available *still debating usefulness, JSONAPI may be better*
      
  - base user aware view class
    
    - base class for requests that need auth
      
  - base cornice resource
  - base static resource
  - base page resource *this is almost good enough*
    
    - send the html page that runs the app **complete**
    - use template to fill the head with links and meta info
    - handle permissions for access to app *send auth_token as query param?*
      
- server side validation **still needed**
  
  - use colander to build schemas for validation (or JSONSchema?)
    
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

