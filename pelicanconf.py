#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Site
AUTHOR = u'r.4ntix Blue'
SITENAME = u"r.4ntix Blue's Noise Player"
THEME = "themes/rocks"

# TIME & LANG
TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = u'cn'

# Date format
DATE_FORMATS = {
    'en': '%a, %d %b %Y',
    'cn': '%Y年%m月%d日',
}

# Article URL format
ARTICLE_URL = '{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# Pages URL format
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Social
SOCIAL = (('Readability', 'https://www.readability.com/r4ntix/'),
          ('Instagram', 'http://instagram.com/r4ntix'),
          ('Twitter', 'https://twitter.com/r4ntix'),
          ('Google+', 'https://plus.google.com/112109872395334308066'),)

# Pagination
DEFAULT_PAGINATION = False

# set static file path for {attach}
STATIC_PATHS = ['']

# Active Categroy in index.html
ACTIVE_CATEGORY = 'Writings'
