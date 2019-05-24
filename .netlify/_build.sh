#!/bin/sh

set -e

pipenv run invoke blog.build-all --production
