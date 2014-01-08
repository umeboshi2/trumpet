haberdashery
============

[![Build Status](https://travis-ci.org/umeboshi2/haberdashery.png?branch=master)](https://travis-ci.org/umeboshi2/haberdashery)

Introduction
--------------


Common accessories for web applications

The purpose of this project is to provide a common code base for 
providing command static resources, such as css and javascript, 
for my pyramid projects.  This is basically just a metapackage 
that depends on many javascript libraries that are deployed with 
fanstatic.  I create the css files with compass, and while a 
framework is here to compile css with compass, as well as compile 
javascript using coffee, this is usually done at the project level.  
The framework here only provides a reference for how this can 
be done in the project.

Also, with regards to generating css, the sass/partials directory 
is used as a set of components where resources are built.  This 
directory is symlinked in the sass directory of my projects, which is 
what I will be doing until I find a better method of using the compenents, 
or spend the time to create mixins.

Setup
======

Setup Compass
----------------

Make sure rubygems is on your system:
```sh
sudo apt-get install rubygems
```


Setup local gem environment:

```sh
mkdir -p ~/local/gems
```
Add to ~/.bashrc:

```sh
#setup gems if directory exists
if [ -d ~/local/gems ]; then
    export GEM_HOME=~/local/gems
    export PATH=~/local/gems/bin:$PATH
fi
```
Source the bashrc or spawn another shell and install the gems:

```sh
gem install compass
gem install susy
gem install sassy-buttons
gem install bootstrap-sass
gem install compass-ui
```

In the haberdashery directory, prepare and compile css:

```sh
python generate-scss.py
compass compile
```


Setup NodeJS
-------------

Get nodejs for debian
--------------------------

For debian, build a current version of nodejs using
the build scripts in this repository:

https://github.com/mark-webster/node-debian

Follow the instructions to build the debian package, 
then install it.

Then, install these packages globally:

```sh
sudo npm install -g coffee-script
sudo npm install -g grunt-cli
sudo npm install -g bower
```

Build Haberdashery
--------------------

In the project directory, get the packages for grunt:

```sh
npm install
```

Then install the bower packages:

```sh
bower install
```

Bower packages can contain whole git repositories, which can 
be excessive when deploying a python package of static resources.  I 
have written a script that helps to deploy only what is needed from 
the bower components.  The script is not very smart, but handles any
bower package that points to a single file, or list of files very well.


```sh
python prepare-bower-components.py
```

Next, we need some google fonts.  We need the requests package 
for python to run the next script.  Either install it system wide:

```sh
sudo apt-get install python-requests
```

or install it into your virtualenv:

```sh
pip install requests
```

 
Then download the fonts from google by running a python 
script:

```sh
python get-google-fonts.py
```

This will install the fonts in the haberdashery package 
directory.


run grunt

```sh
grunt
```

make package

```sh
python setup.py (develop/install/sdist)
```

 
CSS Framework
================


-  [Compass](http://compass-style.org/):  
   Compass is the tool I use to generate my CSS resources.  The CSS 
   specification has no definitios for variables, forcing many web 
   developers to make class names such as "green" and then add CSS 
   code like this:
   
        .green {
		background-color: green;
		}
			   
   But what the developer really needs is something more along this 
   idea:
   
        .warn {
		background-color: $warning-background;
		}
		   
   . . . which helps to simplify the structure of the CSS and remove some 
   of the bad hacks that are used to workaround the deficiencies of 
   the CSS specification.

-  [Susy](http://susy.oddbird.net/):
   Susy is a grid layout system that will allow for responsive webpages.  I 
   am not using this anymore, as bootstrap is currently handling the 
   responsive grid layout, but Susy is superior to bootstrap and since I 
   am also using bootstrap-sass, I feel that I can eventually reimplement 
   the bootstrap grid layout in Susy.

-  [Sassy Buttons](http://jaredhardy.com/sassy-buttons/): 
   This is a collection of mixins and defaults that help a developer make
   custom buttons very easily.

-  [Bootstrap for Sass](https://github.com/thomas-mcdonald/bootstrap-sass): 
   This wonderful package allows me to refrain from using the css that is 
   provided with bootstrap and quickly make a custom version that I can 
   integrate more closely with other objects on the page.  Having bootstrap 
   in this form allows me to adjust how bootstrap operates and allows me 
   to only choose the parts I need (Currently everything is included).
   
-  [FontAwesome](http://fontawesome.io/):
   Instead of just using the basic css, I have chosen to use the 
   fontawesome-sass distribution.  This provides scalable vector icons
   to websites.
   
-  [Compass UI](https://github.com/patrickward/compass-ui): 
   This compass plugin provides the ability to generate jQueryUI themes
   with a minimum of effort.  I have spent hours on the themeroller before
   trying to create a custom theme that would match the general colors that 
   I use on a web page.  With this plugin, all I have to do is set the 
   variables to correspond to the color variables that I use elsewhere on the 
   page and I instantly get themed widgets that don't look like they came 
   from another site.
   

Basic Javascript Libraries
===============================

-  [Requirejs](http://requirejs.org):
   Required.
   
-  [jQuery](http://jquery.com/): 
   jQuery is a very good for selecting and maninpulating elements in the DOM.

-  [jQuery User Interface](http://jqueryui.com/): 
   jQueryUI is used for the fullcalendar widget, as well as for dialog boxes 
   and other user interface elements that aren't used through boostrap.  The 
   corresponding styles are maintained with compass.

-  [Bootstrap v3](http://getbootstrap.com/): 
   Bootstrap is a CSS/Javascript framework used to help make responsive 
   websites.  Bootstrap was selected to be used in order to serve to 
   mobile devices.  The CSS is handled through compass with bootstrap-sass.
   
-  [Underscore.js](http://underscorejs.org/): 
   Underscore is a library full of useful utilities, and like jqueryui, is 
   depended upon by other javascript libraries I use.

-  [Backbone.js](http://backbonejs.org/): 
   Backbone is an excellent library that provides an api to make very 
   rich views tied to models that are seamlessly synchronized with 
   the server via a REST interface.

-  [FullCalendar](http://arshaw.com/fullcalendar/): 
   FullCalendar is a very good library that provides an interactive 
   calendar where events can be retrieved dynamically and grouped, 
   colored, or otherwised styled in many ways.  The calendar provides 
   monthly, weekly, and daily view models to interact with.

-  [Ace Editor](http://ace.c9.io/#nav=about): 
   The ACE editor is a good text editor that is very useful for 
   editing html, css, java/coffee scripts, and other formats that
   aren't being used yet.
   
-  [CoffeeScript](http://coffeescript.org/):
   I am currently experimenting executing coffeescript on the client 
   using the browser to compile the code.  While compilation is 
   generally quick on the browser, the size of the compiler (196KB, and 
   already minified) encourages me to consider implementing server side 
   compilation.
  
-  [Teacup](http://goodeggs.github.io/teacup/):
   "Teacup is templates in CoffeeScript."  -- nuff said
   http://en.wikipedia.org/wiki/Domain-specific_language
  



Misc Javascript
=================

This section lists libraries and widgets that I am experimenting with:


Knockback
http://kmalakoff.github.io/knockback/

TinyMCE
http://www.tinymce.com/

Modernizr
http://modernizr.com/

EJS Templating (I was using this until found out about teacup)




Creating CSS
-------------

This project is configured to make use of compass to compile sass/scss stylesheets into css to be deployed through fanstatic.


Using Javascript
--------------------

This project is using coffeescript to generate javascript to be 
deployed.  The coffee command is best installed by installing the 
nodejs packages from sid (I used apt pinning for this), then using the 
npm installer to install coffee to /usr/local. (more info on this when I 
remember what I did).

Coffee Script: http://coffeescript.org/




Other Packages
---------------------

https://github.com/umeboshi2/js.jquery

This package uses jQuery2 to provide the jquery resource.  This is 
meant to be a drop-in replacement for js.jquery, and using 
this modification shouldn't be required for the rest of the 
code to work properly.

https://github.com/umeboshi2/js.ace

This update was necessary for EJS templates.  I created an update 
script that helps to upgrade the package periodically.


https://github.com/umeboshi2/js.deform

I have been upgrading to deform version 2.  This package is 
currently just a mirror of https://github.com/dairiki/js.deform .


https://raw.github.com/PaulUithol/Backbone-relational/master/backbone-relational.js


http://pathable.github.io/supermodel/



Minified Resources
---------------------

The watch script will automatically minify every scss/sass and 
coffee file that is created or modified.  In order to do this, you 
need to install yui-compressor.  I am using the package from 
wheezy to provide this.

New System
-------------------

Fanstatic has been removed completely.  All javascript dependencies are 
now being maintained with javascript development tools.  Package management 
is community driven and operated.  By partitioning the project to have the 
appropriate community help maintain the packages and dependencies, I firmly 
feel that the project can be more easily updated and maintained.


TODO
------------

- Clean stdlib directory.  Make sure bower package exists for each resource.

- Start tracking css selector usage and use this to make smaller stylesheets.

- Use requrirejs optimizer on each app's main.js and build single 
  concatenated file of app tree.
