Some Former Trumpet Documentation
========================================


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

Old News
-----------

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

