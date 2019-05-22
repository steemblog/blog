# -*- coding:utf-8 -*-

import re
import html

from bs4 import BeautifulSoup
from markdown import markdown


REGEX_IMAGE_URL = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)\.(jpg|jpeg|png|gif|svg)"


class SteemMarkdown:

    def __init__(self, text):
        self.text = text

    def get_top_image(self, regex=False):
        if regex:
            # follow markdown format
            m = re.search(r"!\[(.*)\]\((\S+)\)", self.text)
            if m:
                pic_url = m.group(2)
                return pic_url

            # follow url format
            m = re.search(REGEX_IMAGE_URL, self.text)
            if m:
                pic_url = m.group(0)
                return pic_url
        else:
            links = self.get_img_links()
            if links and len(links) > 0:
                return links[0]

        return None

    def get_rendered_text(self):
        """ Converts a markdown string to plaintext """

        # md -> html -> text since BeautifulSoup can extract text cleanly
        html = markdown(self.text)

        # remove code snippets
        html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
        html = re.sub(r'<code>(.*?)</code >', ' ', html)

        # extract text
        soup = BeautifulSoup(html, "html.parser")
        text = ''.join(soup.findAll(text=True))

        text = re.sub(REGEX_IMAGE_URL, '', text)

        return text

    def _get_valid_link(self, url):
        url = url.strip()
        if url[-1] == ")":
            url = url[:-1]
        # unescape HTML chars
        return html.unescape(url)

    def _is_img_link(self, url):
        m = re.match(REGEX_IMAGE_URL, url)
        return m is not None

    def get_links(self, regex=True):
        body = self.text

        if regex:
            # text = re.sub('<[^<]+?>', ' ', str(self.text))
            links = re.findall(URL_REGEX, body)
        else:
            # md -> html -> text since BeautifulSoup can extract text cleanly
            html = markdown(body)
            # extract links
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.findAll("a")
            links = [tag.get("href") for tag in tags]

        if len(links) > 0:
            links = [self._get_valid_link(link) for link in links if link is not None]

        return links or []

    def get_img_links(self):
        body = self.get_steem_markdown()

        # md -> html -> text since BeautifulSoup can extract text cleanly
        html = markdown(body)
        # extract links
        soup = BeautifulSoup(html, "html.parser")
        tags = soup.findAll("img")
        links = [tag.get("src") for tag in tags]

        if len(links) > 0:
            links = [self._get_valid_link(link) for link in links if link is not None]

        return links or []

    def get_steem_markdown(self):
        text = self.text
        text = re.sub(r"(?P<url>" + REGEX_IMAGE_URL + r")(?P<space>\s+)", r"![](\g<url>)\g<space>", text)
        return text
