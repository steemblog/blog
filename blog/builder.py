# -*- coding:utf-8 -*-

import os
import subprocess
import requests

from steem.comment import SteemComment
from steem.account import SteemAccount
from steem.settings import settings, STEEM_HOST
from data.reader import SteemReader
from utils.logging.logger import logger
from blog.message import get_message


BLOG_ORGANIZATION = "steemblog"
BLOG_AVATAR = "https://avatars0.githubusercontent.com/u/50857551?s=200&v=4"
BLOG_FAVICON = "https://www.easyicon.net/api/resizeApi.php?id=1185564&size=32"

CONFIG_FILE = "_config.yml"
CONFIG_THEME_FILE = "_config.theme.yml"

SOURCE_BRANCH = "source"
SOURCE_FOLDER = "source"
POSTS_FOLDER = "_posts"
BLOG_CONTENT_FOLDER = "./{}/{}".format(SOURCE_FOLDER, POSTS_FOLDER)


class BlogBuilder(SteemReader):

    def __init__(self, account=None, tag=None, days=None, host="github"):
        SteemReader.__init__(self, account=account, tag=tag, days=days)

        self.host = host

        # create blog folder
        self.blog_folder = os.path.join(BLOG_CONTENT_FOLDER, self._get_subfolder())

        self.folder_created = False

    def get_name(self):
        name = "blog"
        target = self.account or self.tag
        return "{}-{}-{}".format(name, target, self._get_time_str())

    def is_qualified(self, post):
        return True

    def _get_subfolder(self):
        # create blog folder
        subfolder = None
        if self.account:
            subfolder = os.path.join("account", self.account)
        elif self.tag:
            subfolder = os.path.join("tag", self.tag)

        return subfolder

    def _get_content_folder(self):
        if not self.folder_created and not os.path.exists(self.blog_folder):
            os.makedirs(self.blog_folder)
        self.folder_created = True
        return self.blog_folder

    def _write_content(self, post):
        folder = self._get_content_folder()
        c = SteemComment(comment=post)

        # retrieve necessary data from steem
        title = post.title.replace('"', '')
        permlink = post["permlink"]
        body = c.get_compatible_markdown()
        date_str = post.json()["created"]
        date = date_str.replace('T', ' ')
        tags = "\n".join(["- {}".format(tag) for tag in c.get_tags()])
        category = c.get_tags()[0]
        thumbnail = c.get_pic_url() or ''
        url = c.get_url()

        # build content with template
        template = get_message("blog", footer=True)
        content = template.format(title=title, permlink=permlink, date=date,
                                  tags=tags, category=category,
                                  thumbnail=thumbnail, body=body, url=url)

        # write into MD files
        filename = os.path.join(folder, "{}_{}.md".format(date_str.split('T')[0], permlink))
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info("Download post [{}] into file {}".format(title, filename))

    def download(self):
        if len(self.posts) == 0:
            self.get_latest_posts()
        if len(self.posts) > 0:
            for post in self.posts:
                self._write_content(post)
        return len(self.posts)

    def _get_domain(self):
        if self.host == "netlify":
            return "netlify.com"
        else: # self.host == "github"
            return "github.io"

    def _get_blog_url(self):
        return "https://{}.{}/@{}".format(BLOG_ORGANIZATION, self._get_domain(), self.account)

    def _get_repo(self, prefix=True):
        repo = "{0}/{0}.github.io".format(BLOG_ORGANIZATION)
        if prefix:
            repo = "https://github.com/" + repo
        return repo

    def update_config(self, incremental=False):
        if not self.account:
            return

        domain = self._get_domain()
        organization = BLOG_ORGANIZATION
        logo = BLOG_AVATAR
        favicon = BLOG_FAVICON

        language = settings.get_env_var("LANGUAGE") or "en"

        a = SteemAccount(self.account)
        author = self.account
        name = a.get_profile("name") or ""
        avatar = a.avatar() or ""
        # about = a.get_profile("about") or ""
        location = a.get_profile("location") or ""
        website = a.get_profile("website") or ""
        incremental = "true" if incremental else "false"

        # build config file with template
        template = get_message("config")
        config = template.format(organization=organization, domain=domain,
                                 language=language, name=name, author=author,
                                 incremental=incremental)
        filename = CONFIG_FILE
        with open(filename, "w", encoding="utf-8") as f:
            f.write(config)
        logger.info("{} file has been updated for the account @{}".format(filename, author))

        # build config theme file with template
        template = get_message("config.theme")
        config = template.format(organization=organization,
                                 favicon=favicon, logo=logo,
                                 author=author, name=name, location=location,
                                 avatar=avatar, website=website)
        filename = CONFIG_THEME_FILE
        with open(filename, "w", encoding="utf-8") as f:
            f.write(config)
        logger.info("{} file has been updated for the account @{}".format(filename, author))

    def _blog_exists(self):
        if not self.account:
            return False

        blog_url = self._get_blog_url()
        r = requests.get(blog_url)
        if r.ok:
            logger.info("The blog [{}] already exists".format(blog_url))
            return True
        else:
            logger.info("The blog [{}] doesn't exist".format(blog_url))
            return False

    def fetch_source(self):
        github_pat = settings.get_env_var("GITHUB_PAT") or None
        if github_pat:
            github_pat += "@"
        else:
            github_pat = ""

        subfolder = os.path.join(POSTS_FOLDER, self._get_subfolder())
        git_clone_cmd = "git clone --depth 1 --branch {} --single-branch https://{}github.com/{}.git {}".format(SOURCE_BRANCH, github_pat, self._get_repo(prefix=False), SOURCE_FOLDER)

        git_init_cmds = [
            "git init",
            "git remote add origin https://{}github.com/{}.git".format(github_pat, self._get_repo(prefix=False))
        ]

        git_sparse_checkout_cmds = [
            "git config core.sparsecheckout true",
            "echo {}/ >> .git/info/sparse-checkout".format(subfolder),
            # "git read-tree -mu HEAD"
            "git pull origin {} --depth 1".format(SOURCE_BRANCH)
        ]

        # os.system(git_clone_cmd)
        os.mkdir(SOURCE_FOLDER)
        os.chdir(SOURCE_FOLDER)
        for cmd in git_init_cmds:
            os.system(cmd)
        for cmd in git_sparse_checkout_cmds:
            os.system(cmd)
        os.chdir("..")

        logger.info("Cloned source repo into workspace: {}".format(SOURCE_FOLDER))

    def list_new_posts(self):
        os.chdir(SOURCE_FOLDER)
        os.system("git add --all *")
        res = subprocess.run(['git', 'diff', '--name-only', '--cached'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        os.chdir("..")

        paths = [path for path in res.split("\n") if len(path) > 0]
        count = len(paths)
        logger.info("{} new posts are found:\n{}".format(count, res))
        return count

    def set_smart_duration(self):
        if not self.account:
            return

        if self._blog_exists():
            self.days = settings.get_env_var("DURATION") or 1.5
            logger.info("The download duration has been set to {} days".format(self.days))
        else:
            self.days = None
            logger.info("The download duration has been expanded to the entire lifetime of the account")


