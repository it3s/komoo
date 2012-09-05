# -*- coding: utf-8 -*-
from fabric.api import local


def tests(test_type='both'):
    """Run our tests using nose for python and phantomjs for javascript"""
    py_test = 'nosetests -v'
    js_test = 'phantomjs static/tests/run-qunit.js templates/tests.html'
    if test_type in ['py', 'both']:
        local(py_test)
    if test_type in ['js', 'both']:
        local(js_test)


def coverage():
    """Run tests with coverage analysis and outputs in HTML on docs/cover"""
    local(
        'nosetests --with-coverage --cover-html --cover-html-dir=docs/cover/')


def develop():
    """Start watchers"""
    local('nosy --config=nose_config.cfg')


def update_requirements():
    """Updates pip requirements file"""
    local('pip freeze > requirements.txt')

