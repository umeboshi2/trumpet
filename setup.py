#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'hornstone',
    'pyramid >= 1.9a',
    'pyramid_tm',
    'plaster_pastedeploy',
    'zope.sqlalchemy',
    'pyramid-beaker',  # session management
    'pyramid-mako',
    'cornice',         # REST views
    'waitress',
    'bcrypt',
    'python-dateutil',
    # testing below
    'querystring_parser',
    # 'versiontools',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup_requirements = [
    'pytest-runner',
    # TODO(umeboshi2): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
    # TODO: put package test requirements here
]

setup(
    name='trumpet',
    version='0.2.8',
    description="Build a website with pyramid",
    long_description=readme + '\n\n' + history,
    author="Joseph Rawson",
    author_email='joseph.rawson.works@gmail.com',
    url='https://github.com/umeboshi2/trumpet',
    packages=find_packages(include=['trumpet', 'trumpet.*']),
    entry_points={
        'paste.app_factory': [
            'main = trumpet:main',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license="UNLICENSED",
    zip_safe=False,
    keywords='trumpet',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
