# Trumpet Documentation

[![Build Status](https://travis-ci.org/umeboshi2/trumpet.png?branch=master)](https://travis-ci.org/umeboshi2/trumpet)




## Abstract

## New System

Fanstatic has been removed completely.  All javascript dependencies are 
now being maintained with javascript development tools.  Package management 
is community driven and operated.  By partitioning the project to have the 
appropriate community help maintain the packages and dependencies, I firmly 
feel that the project can be more easily updated and maintained.

## Vagrant

Using vagrant to host development environment.

Install virtualbox

Install vagrant 1.5.1

```sh
wget https://dl.bintray.com/mitchellh/vagrant/vagrant_1.5.1_x86_64.deb
dpkg -i vagrant_1.5.1_x86_64.deb

# or

wget https://dl.bintray.com/mitchellh/vagrant/vagrant_1.5.1_i686.deb
dpkg -i vagrant_1.5.1_i686.deb
```

or

Click [here](https://dl.bintray.com/mitchellh/vagrant/vagrant_1.5.1.msi) 
for windows.


then,

```sh
vagrant plugin install vagrant-vbguest

vagrant up

vagrant ssh

# within vagrant VM
cd /vagrant

# install node packages
npm install

# install bower components
bower install

# run grunt to build static assets
grunt

# build source dist package
python setup.py sdist
```

## TODO

- Integrate sucker-compass.  https://github.com/adambom/sucker-compass

- Admin section will handle some site images and text.

  + make thumbnail images

  + better list images page

- start using cryptacular and/or SRP

- add exception logging

- start making REST interface

  + cornice uses url-dispatch, but can possibly work alongside
    traversal in a hybrid manner.

- compare python-magic and filemagic

- add exception pages

- replace fanstatic with webassets


## Notes

### Making an action button

- make a 'div' with 'action-button' in the class

- also name the div in either the class or id, so it
 can be selected with jquery

- in the div, make a hidden input with value=url

- make sure that the action-button is imported in css

- make jquery script that performs action on click

  + example:  window.location = url







## haberdashery

Common Accessories for web applications

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



## Misc Javascript

This section lists libraries and widgets that I am experimenting with:


Knockback
http://kmalakoff.github.io/knockback/

TinyMCE
http://www.tinymce.com/

Modernizr
http://modernizr.com/

EJS Templating (I was using this until found out about teacup)


## More Links

Pyramid Framework: http://www.pylonsproject.org/

SQLAlchemy: http://www.sqlalchemy.org/

Mako Templates: http://www.makotemplates.org/

Icons: http://www.sireasgallery.com/ (trumpet icon)

## more links

Pyramid Framework: http://www.pylonsproject.org/

SQLAlchemy: http://www.sqlalchemy.org/

Mako Templates: http://www.makotemplates.org/

Icons: http://www.sireasgallery.com/ (trumpet icon)


## Creating CSS

This project is configured to make use of compass to compile sass/scss stylesheets into css to be deployed through fanstatic.


## Using Javascript

This project is using coffeescript to generate javascript to be 
deployed.  The coffee command is best installed by installing the 
nodejs packages from sid (I used apt pinning for this), then using the 
npm installer to install coffee to /usr/local. (more info on this when I 
remember what I did).

Coffee Script: http://coffeescript.org/








## TODO 2

- Start tracking css selector usage and use this to make smaller stylesheets.

- Use requrirejs optimizer on each app's main.js and build single 
  concatenated file of app tree.


