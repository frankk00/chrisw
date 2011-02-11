#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import uhome, userui, photo
from conf import settings
from google.appengine.ext import webapp

class V2UIHandler(webapp.RequestHandler):
  def get(self):
    # path = os.path.join(os.path.dirname(__file__), '../templates/base.html')
    # self.response.out.write(template.render(path, {'user': 'andyzhau'}))
    from api.shortcuts import render_to_string
    from duser.auth import get_current_user
    self.response.out.write(render_to_string('base.html', {'user': get_current_user()}))

class RootHandler(webapp.RequestHandler):
  """docstring for RootHandler"""
  def get(self):
    """Redirect the root request to the default url"""
    self.redirect(settings.DEFAULT_HOME, True)
    

class URLStripper(webapp.RequestHandler):
  def get(self, naked_url):
    """docstring for get"""
    self.redirect(naked_url, True)

apps = uhome.apps + userui.apps + photo.apps + [('/v2', V2UIHandler),] \
  +[('/', RootHandler),] + [('(.*)/', URLStripper),]

def create_login_url(back_url):
  """docstring for create_login_url"""
  import urllib
  return settings.LOGIN_URL + "?back_url=" + urllib.quote_plus(back_url)

