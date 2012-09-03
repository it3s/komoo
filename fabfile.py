# -*- coding: utf-8 -*-
from fabric.api import local


def tests():
    """Run our tests using nose"""
    local('nosetests -v')


def coverage():
    """Run tests with coverage analysis and outputs in HTML on docs/cover"""
    local(
        'nosetests --with-coverage --cover-html --cover-html-dir=docs/cover/')


def update_requirements():
    """Updates pip requirements file"""
    local('pip freeze > requirements.txt')

