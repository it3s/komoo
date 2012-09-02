# -*- coding: utf-8 -*-
import subprocess


def _sh(command):
    subprocess.Popen(command.split())


def tests():
    _sh('python -m unittest discover . \'*_test.py\'')
    # _sh('sensible-browser ./templates/tests.html')
