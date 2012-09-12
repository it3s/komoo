# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

app = Blueprint('main', 'main')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('tests/')
def tests():
    """This view loads our javascrit test suite"""
    return render_template('tests.html')
