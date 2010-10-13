#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import settings
import uhome, userui, photo
from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
  def get(self):
    # path = os.path.join(os.path.dirname(__file__), '../templates/base.html')
    # self.response.out.write(template.render(path, {'user': 'andyzhau'}))
    from api.shortcuts import render_to_string
    from duser.auth import get_current_user
    self.response.out.write(render_to_string('base.html', {'user': get_current_user()}))

class URLStripper(webapp.RequestHandler):
  def get(self, naked_url):
    """docstring for get"""
    self.redirect(naked_url, True)

apps = uhome.apps + userui.apps + photo.apps + [('/', MainHandler),] + [('(.*)/', URLStripper),]

def create_login_url(back_url):
  """docstring for create_login_url"""
  import urllib
  return settings.LOGIN_URL + "?back_url=" + urllib.quote_plus(back_url)

