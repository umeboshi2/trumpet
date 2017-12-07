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

Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

