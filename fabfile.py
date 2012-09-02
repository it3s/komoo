# -*- coding: utf-8 -*-
from fabric.api import local


def tests():
    local("python -m unittest discover . '*_tests.py'")
    # _sh('sensible-browser ./templates/tests.html')
