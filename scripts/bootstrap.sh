#! /usr/bin/env sh

pip install -r requirements.txt

sudo apt-get install mongodb nodejs npm rubygems redis-server -y

sudo npm install -g coffee-script@1.2
sudo npm install -g optimist watcher_lib commander coffee-watcher

sudo gem install sass

git submodule init
git submodule update

