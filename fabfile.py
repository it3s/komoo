# -*- coding: utf-8 -*-
from fabric.api import local


def tests(test_type='both'):
    """Run our tests using nose for python and phantomjs for javascript"""
    py_test = 'nosetests -v --nocapture'
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
    # compilers
    local('coffee-watcher -d static/ -p "" &')
    local('sass --watch static/css/ &')

    # test runners
    local('nosy --config=nose_config.cfg &')
    local('sleep 3')
    local('python lib/phantomjs-notify/watcher.py &')


def update_requirements():
    """Updates pip requirements file"""
    local('pip freeze > requirements.txt')


def kill_background_tasks():
    for task in ['nosy', 'watcher.py', 'coffee-watcher', 'sass']:
        local(
            "ps -eo pid,args | grep %s | grep -v grep | "
            "cut -c1-6 | xargs kill" % task)


def run():
    local('python komoo.py')
