#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'James Casbon'
SITENAME = u'casbon.me'
SITEURL = ''

# ARTICLE_URL  = '{slug}'
# ARTICLE_SAVE_AS = '{slug}'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          )

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/casualbon'),
          ('github', 'https://github.com/jamescasbon'),)

DEFAULT_PAGINATION = 3

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "pelican-mockingbird"
# THEME = "built-texts"


GITHUB_URL = "https://github.com/jamescasbon"

FILES_TO_COPY = (('extra/README.md', 'README.md'), )
