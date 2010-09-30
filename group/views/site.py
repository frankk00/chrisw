#!/usr/bin/env python
# encoding: utf-8
"""
site.py

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging
import settings

from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms

from duser.auth import get_current_user
from api.webapp import *
from group.models import *
from groupui import GroupForm

class SiteUI(PermissionUI):
  """docstring for GroupUI"""
  def __init__(self, site):
    super(SiteUI, self).__init__(site)
    self.site = site
    
  @view_method
  def view(self):
    return template('site_display.html', locals())
  
  @view_method
  def create_group(self):
    form = GroupForm()
    post_url = '/group/new'
    return template('item_new', locals())
  
  def create_group_post(self, request):
    form = GroupForm(data=request.POST)
    if form.is_valid():
      new_group = form.save(commit=False)
      new_group.create_user = get_current_user()
      new_group.put()
      return redirect('/group/%d' % new_group.key().id())
    return template('item_new', locals())

class SiteHandler(webapp.RequestHandler):
  """docstring for SiteHandler"""
  
  def get_impl(self, site):
    raise Exception("Have not implemented")
  
  def post_impl(self, site, request):
    return self.get_impl(site)
  
  @api_enabled
  def get(self):
    return self.get_impl(SiteUI(Site()))
  
  @api_enabled
  def post(self):
    return self.post_impl(SiteUI(Site()), self.request)
    
class SiteViewHandler(SiteHandler):
  """docstring for SiteViewHandler"""
  def get_impl(self, site):
    return site.view()

class SiteNewGroupHandler(SiteHandler):
  """docstring for SiteNewGroupHandler"""
  def get_impl(self, site):
    return site.create_group()
  
  def post_impl(self, site, request):
    return site.create_group_post(request)


apps = [(r'/group', SiteViewHandler),
        (r'/group/new', SiteNewGroupHandler),
        ]