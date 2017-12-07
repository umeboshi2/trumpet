Older Web Views Documentation
=============================

Webviews
--------

A Webview is a name created to denote a single page application. Trumpet
is being geared to become a library to help create websites where
most/all pages are apps. I have managed to shrink the html page served
by pyramid to a very small head with one script tag loading requirejs
and pointing to the loader for the app. I would love to use another name
for this, but naming is probably the hardest part of development.

Page Layouts
~~~~~~~~~~~~

Before switching to the SPA paradigm of thought, every page was rendered
with a template that depended on the presence of a layout model. The
layout model was simply an object with attributes that was applied to a
mako template. The type of each attribute is either text or mako
template. One of my original goals was to store the main layout template
in the database, as well as css and javascript, to allow the end
user/admin to customize the site without updating the code.

Server vs. Client
~~~~~~~~~~~~~~~~~

Mako templates are very powerful, allowing the author to wield the full
power of python when rendering the template. In fact, the templates are
versatile enough to bypass writing code in the view callable and put all
the logic in the template, although this is generally not the wisest
thing to do. The largest problem with using the mako templates is that
the code is executed server side, preventing me from being able to
protect the service from mistakes or malice. I thought about using a
more restrictive template system, but soon realized that the inherent
problem was the server side rendering, and the server templates would
either have to be too limited to be of more than cosmetic use, or
flexible enough to bypass the policy of the server.

This is where client side templating comes to the rescue. With client
side templates, it is far more difficult to endanger the service that is
being provided. I am expecting the worst of the problems to be
dysfunctional pages, although the admin pages that edit the templates
should always work. I also see a very slim (I hope!) possibility that
bad templates could cause a denial of service, but I don't expect this
to be a problem that occurs often.

Being less familiar with javascript than with python, I had to search
and compare templating styles. I started with underscore templates, but
found them to be very limiting. I then started using EJS templates, and
found them to be very similar to mako templates, although not as
versatile. Nevertheless, I settled on using EJS templates for trumpet.

After believing I was happy with using EJS templates, I was looking
around the stackoverflow forums to find a solution that I was having
with CoffeeScript and learned about teacup. Teacup is a domain specific
language that works very well as a templating system. With teacup, not
only do you have the full flexibility of javascript when rendering the
template, you are also using coffeescript to define the template, which
is far more elegant than anything else I have seen on either the python
or javascript sides. I did like how concise jade is, but I feel that
teacup will be a better fit for trumpet.

REST
~~~~

The general idea behind REST isn't really hard to understand. It was
having to unlearn the way by which much of the web had already been
operating for years. I spent many years knowing nothing of PUT and
DELETE, but only being familiar with GET and POST, which I naively
treated (loosely) as read/write methods. Now that I look back (and not
very far either) I was often using GET to perform both deletions of
single objects, as well as attaching relations together.

After learning REST, my ability to write arbitrary url's to perform a
function has been severely hampered, and this is a good thing. I now
have only four verbs that I am able to use, and I am completely
restricted from putting verbs in the url, or even identifying the url as
an action. These restrictions help keep the web services well structured
and coherent. In fact, a good REST API decouples the server from the
browser, allowing a larger variety of clients to have access to the
services.

Static Resources
~~~~~~~~~~~~~~~~

Managing static resources can become very messy the more involved a
project becomes in using them. The very large variety of javascript
libraries and css frameworks available can be overwhelming. Making sure
that everything fits together and works can be an arduous task. Tracking
upstream dependencies is probably a bit more difficult for a
python/pyramid programmer than it is for a person using rails or nodejs.
I had been (and I am currently still) using fanstatic to help manage
these resources. There are quite a few prepackaged libraries depending
on fanstatic available on the Python Package Index. These packages don't
seem to be in much use, and after updating quite a few of them myself, I
decided to wean myself away from fanstatic. I am currently investigating
webassets, which seems to be a far more robust and capable asset
manager.

Moreover, and more especially with css, it can become very time
consuming to modify two or more upstream css resources to match the
general style of your page.

