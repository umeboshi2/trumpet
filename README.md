 # Trumpet Documentation

[![Build Status](https://travis-ci.org/umeboshi2/trumpet.png?branch=master)](https://travis-ci.org/umeboshi2/trumpet)




## Abstract

Trumpet uses the [Pyramid](http://www.pylonsproject.org/) framework 
to provide services to help build websites.  The goal of this project is 
to provide a more opinionated framework that focuses on [REST](http://en.wikipedia.org/wiki/Representational_state_transfer) resources and provides a 
system to develop [Single Page Applications](http://en.wikipedia.org/wiki/Single-page_application), as well as use some simple ones provided by the 
trumpet package.

A page on the static resources used to build SPA's can be found [here](https://github.com/umeboshi2/trumpet/blob/master/docs/TrumpetStaticResources.md).

## NEWS

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

## Goals

- user management
  - login/logout
  - administer users via REST
  - reflective sqlalchemy code, db should provide minimum user/password tables
- db support
  - common sqlalchemy code for all databases
  - request object with attached sessionmaker
- session management
  - minimal use of cookies
  - use access_token as parameter to all requests requiring authentication
  - policies for session management
    - sessions per user (configure number of sessions a user can have)
    - sessions per device (register devices to user?)
    - session duration
    - session timeout/expiration
  - is beaker good enough?
- view classes
  - basic view classes to be used by all views
    - common methods
    - app settings available
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

  
## Old

Remnants of the old README can be found [here](https://github.com/umeboshi2/trumpet/blob/master/docs/misc.md).
