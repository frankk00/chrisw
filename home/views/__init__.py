#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import usersite, userui, photo, user_stream, front
from conf import settings
from google.appengine.ext import webapp

class RootHandler(webapp.RequestHandler):
  """docstring for RootHandler"""
  def get(self):
    """Redirect the root request to the default url"""
    self.redirect(settings.DEFAULT_HOME, True)
    

class URLStripper(webapp.RequestHandler):
  def get(self, naked_url):
    """docstring for get"""
    self.redirect(naked_url, True)

apps = usersite.apps + userui.apps + photo.apps + user_stream.apps \
  +[('/', RootHandler),] + [('(.*)/', URLStripper),]

def create_login_url(back_url):
  """docstring for create_login_url"""
  import urllib
  return settings.LOGIN_URL + "?back_url=" + urllib.quote_plus(back_url)

