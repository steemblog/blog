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
      'clear': 'clean previous posts before download',
      'production': 'set production mode to download incrementally'
      })
def download(ctx, account=None, tag=None, days=None, debug=False, clear=False, production=False):
    """ download the posts to local by the account """

    if debug:
        settings.set_debug_mode()
    if clear:
        clean(ctx)

    settings.set_steem_node()

    account = account or settings.get_env_var("STEEM_ACCOUNT")
    tag = tag or settings.get_env_var("STEEM_TAG")
    days = days or settings.get_env_var("DURATION")

    builder = BlogBuilder(account=account, tag=tag, days=days)
    # if production:
        # builder.set_smart_duration()
    builder.update_config()
    return builder.download()


@task(help={
      })
def clean(ctx):
    """ clean the downloaded posts """

    os.system("rm -rf source/_posts")


def configure():
    os.system("cp -f _config.theme.yml themes/icarus/_config.yml")


@task(help={
      'debug': 'enable the debug mode',
      })
def build(ctx, debug=False):
    """ build the static pages from steem posts """

    os.system("hexo clean")
    configure()
    build_cmd = "hexo generate"
    if debug:
        build_cmd += " --debug"
    os.system(build_cmd)


@task(help={
      'accounts': 'the accounts of the blogs to download, delimiter is comma',
      'debug': 'enable the debug mode',
      'production': 'set production mode to download incrementally'
      })
def build_all(ctx, accounts=None, debug=False, production=False):
    """ download the posts of all the accounts, and generate pages """

    accounts = accounts or settings.get_env_var("STEEM_ACCOUNTS") or []
    if accounts and len(accounts) > 0:
        for account in accounts.split(","):
            clean(ctx)
            count = download(ctx, account=account, production=production)
            if count > 0:
                build(ctx, debug)


@task(help={
      'debug': 'enable the debug mode',
      })
def test(ctx, debug=False):
    """ build and launch the blog server in local environment """

    build(ctx, debug)
    os.system("hexo server -s")


@task(help={
      })
def deploy(ctx):
    """ deploy the static blog to the GitHub pages """

    build(ctx)
    os.system("hexo deploy")

