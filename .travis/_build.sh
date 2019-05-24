#!/bin/sh

set -e

[ -z "${GITHUB_PAT}" ] && exit 0
[ "${TRAVIS_BRANCH}" != "master" ] && exit 0

pipenv run invoke blog.build-all -h github --production

# if it's cron job, deploy to netlify in the same time
[ "${TRAVIS_EVENT_TYPE}" != "cron" ] && exit 0
pipenv run invoke blog.deploy -h netlify
