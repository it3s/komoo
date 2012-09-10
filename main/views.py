# -*- coding: utf-8 -*-
from flask import Blueprint

app = Blueprint('main', 'main')


@app.route('/')
def index():
    return 'INDEX PAGE'
