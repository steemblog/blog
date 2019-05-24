# -*- coding:utf-8 -*-

import os
import requests

from steem.comment import SteemComment
from steem.account import SteemAccount
from steem.settings import settings, STEEM_HOST
from data.reader import SteemReader
from utils.logging.logger import logger
from blog.message import get_message

BLOG_CONTENT_FOLDER = "./source/_posts"

BLOG_ORGANIZATION = "steemblog"
BLOG_AVATAR = "https://avatars0.githubusercontent.com/u/50857551?s=200&v=4"
BLOG_FAVICON = "https://www.easyicon.net/api/resizeApi.php?id=1185564&size=32"

CONFIG_FILE = "_config.yml"
CONFIG_THEME_FILE = "_config.theme.yml"


class BlogBuilder(SteemReader):

    def __init__(self, account=None, tag=None, days=None, host="github"):
        SteemReader.__init__(self, account=account, tag=tag, days=days)

        self.host = host

        # create blog folder
        if self.account:
            self.blog_folder = os.path.join(BLOG_CONTENT_FOLDER, "account", self.account)
        elif self.tag:
            self.blog_folder = os.path.join(BLOG_CONTENT_FOLDER, "tag", self.tag)
        if not os.path.exists(self.blog_folder):
            os.makedirs(self.blog_folder)

    def get_name(self):
        name = "blog"
        target = self.account or self.tag
        return "{}-{}-{}".format(name, target, self._get_time_str())

    def is_qualified(self, post):
        return True

    def _get_content_folder(self):
        return self.blog_folder

    def _write_content(self, post):
        folder = self._get_content_folder()
        c = SteemComment(comment=post)

        # retrieve necessary data from steem
        title = post.title.replace('"', '')
        body = c.get_compatible_markdown()
        date_str = post.json()["created"]
        date = date_str.replace('T', ' ')
        tags = "\n".join(["- {}".format(tag) for tag in c.get_tags()])
        category = c.get_tags()[0]
        thumbnail = c.get_pic_url() or ''
        url = c.get_url()

        # build content with template
        template = get_message("blog", footer=True)
        content = template.format(title=title, date=date, tags=tags, category=category, thumbnail=thumbnail, body=body, url=url)

        # write into MD files
        filename = os.path.join(folder, "{}_{}.md".format(date_str.split('T')[0], post["permlink"]))
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

    def update_config(self):
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

        # build config file with template
        template = get_message("config")
        config = template.format(organization=organization, domain=domain,
                                 language=language, name=name, author=author)
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

        blog_url = "https://{}.github.io/@{}".format(BLOG_ORGANIZATION, self.account)
        r = requests.get(blog_url)
        if r.ok:
            logger.info("The blog [{}] already exists".format(blog_url))
            return True
        else:
            logger.info("The blog [{}] doesn't exist".format(blog_url))
            return False

    def set_smart_duration(self):
        if not self.account:
            return

        if self._blog_exists():
            self.days = settings.get_env_var("DURATION") or 1.5
            logger.info("The download duration has been set to {} days".format(self.days))
        else:
            self.days = None
            logger.info("The download duration has been expanded to the entire lifetime of the account")


