#! /usr/bin/env sh

# assuming virtualenvwrapper
mkvirtualenv maps2_env
workon maps2_env
setvirtualenvproject
pip install -r requirements.txt
add2virtualenv lib/

