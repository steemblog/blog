#!/bin/sh

set -e

# install python packages
pip install pipenv
pipenv install --pypi-mirror https://pypi.python.org/simple

# install hexo commands
npm install -g hexo-cli
npm install

