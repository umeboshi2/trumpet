Developing trumpet without vagrant
==================================

Setup
-----

I like to use virtualenvwrapper

.. code:: sh

    sudo apt-get install virtualenvwrapper
    mkvirtualenv trumpet
    workon trumpet
    pip install requests

Development packages are needed to install some of the python packages::

.. code:: sh

    sudo apt-get install libpq-dev python-dev libjpeg62-dev libpng12-dev libfreetype6-dev liblcms1-dev python-requests libxml2-dev libxslt1-dev libssl-dev

Next we have to download build and prepare the static resources.

Setup Compass
~~~~~~~~~~~~~

Make sure rubygems is on your system:

.. code:: sh

    sudo apt-get install rubygems

Setup local gem environment:

.. code:: sh

    mkdir -p ~/local/gems

Add to ~/.bashrc:

.. code:: sh

    #setup gems if directory exists
    if [ -d ~/local/gems ]; then
        export GEM_HOME=~/local/gems
        export PATH=~/local/gems/bin:$PATH
    fi

Source the bashrc or spawn another shell and install the gems:

.. code:: sh

    gem install sass -v 3.2.18
    gem install compass -v 0.12.2
    gem install susy -v 1.0.9
    gem install sassy-buttons -v 0.2.6
    gem install bootstrap-sass -v 3.0.2.1
    gem install compass-ui -v 0.0.5

Setup NodeJS
~~~~~~~~~~~~

FIXME: Need better instructions for nodeenv.

Get nodejs for virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: sh

    workon trumpet
    pip install nodeenv
    nodeenv -p

The last statement will download the latest stable version of nodejs and
build it in the python virtual environment so that both virtual
environments can be integrated together.

Install global nodejs packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Then, install these packages globally:

.. code:: sh

    npm install -g coffee-script
    npm install -g grunt-cli
    npm install -g bower

Get packages for grunt
~~~~~~~~~~~~~~~~~~~~~~

In the project directory, get the packages for grunt:

.. code:: sh

    npm install

Get bower components
~~~~~~~~~~~~~~~~~~~~

Then install the bower packages:

.. code:: sh

    bower install

Bower packages can contain whole git repositories, which can be
excessive when deploying a python package of static resources. I have
written a script that helps to deploy only what is needed from the bower
components. The script is not very smart, but handles any bower package
that points to a single file, or list of files very well.

run grunt

.. code:: sh

    grunt

make package

.. code:: sh

    python setup.py (develop/install/sdist)

