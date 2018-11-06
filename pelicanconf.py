#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Slava Kim'
TAGLINE = u'I am here to learn'
SITENAME = u'Yet Another Dev Blog'
SITEURL = '//devblog.me'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

PLUGINS = ['latex']
STATIC = ['images']

# More settings
GOOGLE_ANALYTICS = 'UA-37747647-1'
DISQUS_SITENAME = 'zdeslavablog'
TWITTER_USERNAME = 'imslavko'
#COLLAPSE_COMMENTS = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('GitHub', 'https://github.com/slava'),
          ('Twitter', 'https://twitter.com/imslavko'),
          ('More about me', 'http://slv.io/'),)

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 10

#RELATIVE_URLS = True

# Theme
THEME = './pelican-svbtle'
DISPLAY_CATEGORIES_ON_MENU = False

