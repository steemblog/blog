#!/bin/sh

set -e

# [ -z "${GITHUB_PAT}" ] && exit 0
# [ "${TRAVIS_BRANCH}" != "master" ] && exit 0

# git config --global user.email "${GIT_EMAIL}"
# git config --global user.name "${GIT_USERNAME}"

cd source

if [ -d .git ]; then
  NOW=$(date +"%Y-%m-%d %H:%M:%S %z")
  git commit -m "Source updated: ${NOW}" || true
  git push -q origin source || true
fi

cd ..
