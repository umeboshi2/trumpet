# Trumpet Documentation

[![Build Status](https://travis-ci.org/umeboshi2/trumpet.png?branch=master)](https://travis-ci.org/umeboshi2/trumpet)




## Abstract

Trumpet uses the [Pyramid](http://www.pylonsproject.org/) framework 
to provide services to help build websites.  The goal of this project is 
to provide a more opinionated framework that focuses on [REST](http://en.wikipedia.org/wiki/Representational_state_transfer) resources and provides a 
system to develop [Single Page Applications](http://en.wikipedia.org/wiki/Single-page_application), as well as use some simple ones provided by the 
trumpet package.

A page on the static resources used to build SPA's can be found [here](https://github.com/umeboshi2/trumpet/blob/master/docs/TrumpetStaticResources.md).





## New System

Fanstatic has been removed completely.  All javascript dependencies are 
now being maintained with javascript development tools.  Package management 
is community driven and operated.  By partitioning the project to have the 
appropriate community help maintain the packages and dependencies, I firmly 
feel that the project can be more easily updated and maintained.

## Vagrant

If you desire, you can possibly use virtualenv for [development](https://github.com/umeboshi2/trumpet/blob/master/docs/host-env-setup.md).


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
vagrant plugin install vagrant-salt

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

## Old

Remnants of the old README can be found [here](https://github.com/umeboshi2/trumpet/blob/master/docs/misc.md).

