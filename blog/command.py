# -*- coding:utf-8 -*-

import os, time, random
from invoke import task

from steem.settings import settings
from blog.builder import BlogBuilder


@task(help={
      'account': 'the account of the blogs to download',
      'tag': 'the tag of the blogs to download',
      'days': 'the posts in recent days to fetch',
      'debug': 'enable the debug mode',
      'clean': 'clean previous posts before download',
      'production': 'set production mode to download incrementally'
      })
def download(ctx, account=None, tag=None, days=None, debug=False, clean=False, production=False):
    """ download the posts to local by the account """

    if debug:
        settings.set_debug_mode()
    if clean:
        clean(ctx)

    settings.set_steem_node()

    account = account or settings.get_env_var("STEEM_ACCOUNT")
    tag = tag or settings.get_env_var("STEEM_TAG")
    days = days or settings.get_env_var("DURATION")

    builder = BlogBuilder(account=account, tag=tag, days=days)
    if production:
        builder.set_smart_duration()
    builder.update_config()
    builder.download()


@task(help={
      })
def clean(ctx):
    """ clean the downloaded posts """

    os.system("rm -rf source/_posts")


@task(help={
      })
def build(ctx):
    """ build the static pages from steem posts """

    os.system("cp -f _config.theme.yml themes/icarus/_config.yml")
    os.system("hexo generate --silent")


@task(help={
      'production': 'set production mode to download incrementally'
      })
def build_all(ctx, production=False):
    """ download the posts of all the accounts, and generate pages """

    accounts = settings.get_env_var("STEEM_ACCOUNTS") or []
    if accounts and len(accounts) > 0:
        for account in accounts.split(","):
            clean(ctx)
            download(ctx, account=account, production=production)
            build(ctx)


@task(help={
      })
def test(ctx):
    """ build and launch the blog server in local environment """

    build(ctx)
    os.system("hexo server -s")


@task(help={
      })
def deploy(ctx):
    """ deploy the static blog to the GitHub pages """

    build(ctx)
    os.system("hexo deploy")

