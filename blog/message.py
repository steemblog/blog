# -*- coding:utf-8 -*-

import traceback

from utils.logging.logger import logger


def get_message(id, footer=False):
    return build_message(id, footer)

def build_message(id, footer=False, message_marker=False):
    message = MESSAGES[id]

    if footer and id in FOOTERS:
        message += FOOTERS[id]
    if message_marker:
        message += MESSAGE_ID.format(message_id=id)

    return message

MESSAGE_ID = """
<div message_id=\"{message_id}\"></div>
"""

MESSAGES = {}
FOOTERS = {}

MESSAGES["blog"] = """
---
title: "{title}"
permlink: {permlink}
catalog: true
toc_nav_num: true
toc: true
date: {date}
categories:
- {category}
tags:
{tags}
thumbnail: {thumbnail}
sidebar:
    right:
        sticky: true
widgets:
    -
        type: toc
        position: right
---


{body}
"""

FOOTERS["blog"] = """
- - -

This page is synchronized from the post: [{title}]({url})
"""

MESSAGES['config'] = """
# Hexo Configuration
## Docs: http://hexo.io/docs/configuration.html
## Source: https://github.com/hexojs/hexo/

# Site
# add 'site_title' because 'title' is overriden by the metadata in post
site_title: {name}
title: {name}
subtitle:
description:
author: {author}
language: {language}
timezone:

# URL
## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
url: http://{organization}.{domain}
root: /@{author}/
permalink: :permlink/
permalink_defaults:

# Directory
source_dir: source
public_dir: public/@{author}
tag_dir: tags
archive_dir: archives
category_dir: categories
code_dir: downloads/code
i18n_dir: :lang
skip_render:

# Writing
new_post_name: :title.md # File name of new posts
default_layout: post
titlecase: false # Transform title into titlecase
external_link: true # Open external links in new tab
filename_case: 0
render_drafts: false
post_asset_folder: false
relative_link: false
future: true
highlight:
  enable: true
  line_number: true
  tab_replace:

# Category & Tag
default_category: uncategorized
category_map:
tag_map:

# Date / Time format
## Hexo uses Moment.js to parse and display date
## You can customize the date format as defined in
## http://momentjs.com/docs/#/displaying/format/
date_format: YYYY-MM-DD
time_format: HH:mm:ss

# Pagination
## Set per_page to 0 to disable pagination
per_page: 6
pagination_dir: page

index_generator:
  per_page: 6

archive_generator:
  per_page: 20
  yearly: true
  monthly: true

category_generator:
  per_page: 20

tag_generator:
  per_page: 20

# Extensions
## Plugins: https://github.com/hexojs/hexo/wiki/Plugins
## Themes: https://github.com/hexojs/hexo/wiki/Themes
theme: icarus

# Deployment
## Docs: http://hexo.io/docs/deployment.html
deploy:
  type: git
  repository: https://github.com/{organization}/blog.git
  branch: gh-pages

marked:
  gfm: false

githubEmojis:
  className: not-gallery-item

all_minifier: false
"""

MESSAGES['config.theme'] = """
# Version of the Icarus theme that is currently used
version: 2.3.0
# Path or URL to the website's icon
favicon: {favicon}
# Path or URL to RSS atom.xml
rss:
# Path or URL to the website's logo to be shown on the left of the navigation bar or footer
logo: {logo}
# Open Graph metadata
# https://hexo.io/docs/helpers.html#open-graph
# open_graph:
#     # Facebook App ID
#     fb_app_id:
#     # Facebook Admin ID
#     fb_admins:
#     # Twitter ID
#     twitter_id:
#     # Twitter site
#     twitter_site:
#     # Google+ profile link
#     google_plus:
# Navigation bar link settings
navbar:
    # Navigation bar menu links
    menu:
        Home: /
        Archives: /archives
        Categories: /categories
        Tags: /tags
        About: /about
    # Navigation bar links to be shown on the right
    # links:
    #     Download on GitHub:
    #         icon: fab fa-github
    #         url: 'http://github.com/ppoffice/hexo-theme-icarus'
# Footer section link settings
footer:
    # Links to be shown on the right of the footer section
    links:
        Creative Commons:
            icon: fab fa-creative-commons
            url: 'https://creativecommons.org/'
        Attribution 4.0 International:
            icon: fab fa-creative-commons-by
            url: 'https://creativecommons.org/licenses/by/4.0/'
        # Download on GitHub:
        #     icon: fab fa-github
        #     url: 'http://github.com/ppoffice/hexo-theme-icarus'
# Article display settings
article:
    # Code highlight theme
    # https://github.com/highlightjs/highlight.js/tree/master/src/styles
    highlight: atom-one-dark
    # Whether to show article thumbnail images
    thumbnail: true
    # Whether to show estimate article reading time
    readtime: true
# Search plugin settings
# http://ppoffice.github.io/hexo-theme-icarus/categories/Configuration/Search-Plugins
search:
    # Name of the search plugin
    type: insight
# Comment plugin settings
# http://ppoffice.github.io/hexo-theme-icarus/categories/Configuration/Comment-Plugins
# comment:
#     # Name of the comment plugin
#     type: disqus
#     shortname: hexo-theme-icarus
# Donation entries
# http://ppoffice.github.io/hexo-theme-icarus/categories/Donation/
# donate:
#     -
#         # Donation entry name
#         type: alipay
#         # Qrcode image URL
#         qrcode: /gallery/donate/alipay.png
#     -
#         # Donation entry name
#         type: wechat
#         # Qrcode image URL
#         qrcode: /gallery/donate/wechat.jpg
#     -
#         # Donation entry name
#         type: paypal
#         # Paypal business ID or email address
#         business: paypal@paypal.com
#         # Currency code
#         currency_code: USD
#     -
#         # Donation entry name
#         type: patreon
#         # URL to the Patreon page
#         url: https://www.patreon.com/
# Share plugin settings
# http://ppoffice.github.io/hexo-theme-icarus/categories/Configuration/Share-Plugins
share:
    # Share plugin name
    type: sharethis
    install_url: //platform-api.sharethis.com/js/sharethis.js#property=5ab6f60ace89f00013641890&product=inline-share-buttons
# Sidebar settings.
# Please be noted that a sidebar is only visible when it has at least one widget
sidebar:
    # left sidebar settings
    left:
        # Whether the left sidebar is sticky when page scrolls
        # http://ppoffice.github.io/hexo-theme-icarus/Configuration/Theme/make-a-sidebar-sticky-when-page-scrolls/
        sticky: false
    # right sidebar settings
    right:
        # Whether the right sidebar is sticky when page scrolls
        # http://ppoffice.github.io/hexo-theme-icarus/Configuration/Theme/make-a-sidebar-sticky-when-page-scrolls/
        sticky: false
# Sidebar widget settings
# http://ppoffice.github.io/hexo-theme-icarus/categories/Widgets/
widgets:
    -
        # Widget name
        type: profile
        # Where should the widget be placed, left or right
        position: left
        # Author name to be shown in the profile widget
        author: {author}
        # Title of the author to be shown in the profile widget
        author_title: {name}
        # Author's current location to be shown in the profile widget
        location: {location}
        # Path or URL to the avatar to be shown in the profile widget
        avatar: {avatar}
        # Email address for the Gravatar to be shown in the profile widget
        gravatar:
        # Path or URL for the follow button
        follow_link: 'http://steemit.com/@{author}'
        # Links to be shown on the bottom of the profile widget
        social_links:
            Github:
                icon: fab fa-github
                url: 'http://{organization}.github.io/@{author}'
            Steem:
                icon: fa fa-book
                url: 'http://steemit.com/@{author}'
            Website:
                icon: fa fa-home
                url: '{website}'
        # Cache the widget or not, true or false
        cache: true
    # -
        # Widget name
        # type: links
        # Where should the widget be placed, left or right
        # position: left
        # Links to be shown in the links widget
        # links:
        #     Hexo: 'https://hexo.io'
        #     Bulma: 'https://bulma.io'
    -
        # Widget name
        type: category
        # Where should the widget be placed, left or right
        position: left
        # Cache the widget or not, true or false
        cache: true
    -
        # Widget name
        type: tagcloud
        # Where should the widget be placed, left or right
        position: left
        # Cache the widget or not, true or false
        cache: true
    -
        # Widget name
        type: tag
        # Where should the widget be placed, left or right
        position: left
        # Cache the widget or not, true or false
        cache: true
    -
        # Widget name
        type: toc
        # Where should the widget be placed, left or right
        position: right
        # Cache the widget or not, true or false
        cache: false
    -
        # Widget name
        type: recent_posts
        # Where should the widget be placed, left or right
        position: right
        # Cache the widget or not, true or false
        cache: true
    -
        # Widget name
        type: archive
        # Where should the widget be placed, left or right
        position: right
        # Cache the widget or not, true or false
        cache: true

# Other plugin settings
plugins:
    # Enable page animations
    animejs: true
    # Enable the lightGallery and Justified Gallery plugins
    # http://ppoffice.github.io/hexo-theme-icarus/Plugins/General/gallery-plugin/
    gallery: true
    # Enable the Outdated Browser plugin
    # http://outdatedbrowser.com/
    outdated-browser: true
    # Enable the MathJax plugin
    # http://ppoffice.github.io/hexo-theme-icarus/Plugins/General/mathjax-plugin/
    mathjax: true
    # Show the back to top button on mobile devices
    back-to-top: true
    # Google Analytics plugin settings
    # http://ppoffice.github.io/hexo-theme-icarus/Plugins/General/site-analytics-plugin/#Google-Analytics
    google-analytics:
    #     # Google Analytics tracking id
        tracking_id: # UA-72437521-5
    # Baidu Analytics plugin settings
    # http://ppoffice.github.io/hexo-theme-icarus/Plugins/General/site-analytics-plugin/#Baidu-Analytics
    baidu-analytics:
        # Baidu Analytics tracking id
        tracking_id:
    # Hotjar user feedback plugin
    # http://ppoffice.github.io/hexo-theme-icarus/Plugins/General/site-analytics-plugin/#Hotjar
    hotjar:
    #     # Hotjar site id
        site_id: # 1067642
    # Show a loading progress bar at top of the page
    progressbar: true
    # Show the copy button in the highlighted code area
    clipboard: true
    # BuSuanZi site/page view counter
    # https://busuanzi.ibruce.info
    busuanzi: false
# CDN provider settings
# http://ppoffice.github.io/hexo-theme-icarus/Configuration/Theme/speed-up-your-site-with-custom-cdn/
providers:
    # Name or URL of the JavaScript and/or stylesheet CDN provider
    cdn: jsdelivr
    # Name or URL of the webfont CDN provider
    fontcdn: google
    # Name or URL of the webfont Icon CDN provider
    iconcdn: fontawesome

"""
