#!/usr/bin/env python
# encoding: utf-8
"""
site.py

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging
import settings

from google.appengine.ext import webapp, db
from google.appengine.ext.db import djangoforms

from duser.auth import get_current_user, Guest
from api.webapp import *
from group.models import *
from groupui import GroupForm

class SiteUI(PermissionUI):
  """docstring for GroupUI"""
  def __init__(self, site):
    super(SiteUI, self).__init__(site)
    self.site = site
    user = get_current_user()
    
    if user != Guest:
      groupinfo = UserGroupInfo.all().filter("user_id =", user.key().id()).get()
      if not groupinfo:
        groupinfo = UserGroupInfo(user_id=user.key().id())
        groupinfo.put()
    
    else: groupinfo = None
    self.groupinfo = groupinfo
    
  @view_method
  def view(self, request):
    offset = int(request.get("offset", "0"))
    limit = int(request.get("limit", "20"))
    
    user = get_current_user()
    
    def build_groups(group_keys):
      logging.debug("group_keys " + str(group_keys))
      return [Group.get_by_id(gk) for gk in group_keys]

    recommend_groups = Group.all().fetch(10)
    
    if self.groupinfo:
      # user
      groups = build_groups(self.groupinfo.group_ids)
      
    if not 'groups' in locals():
      # new to group
      groups = recommend_groups

    topics = Topic.all().filter("group IN", groups).order("-update_time").fetch(20)
    
    logging.debug("Fetched recent topics" + str(topics))
    
    return template('site_display.html', locals())
  
  @view_method
  @check_permission("create_group", "Can't create group")
  def create_group(self):
    form = GroupForm()
    post_url = '/group/new'
    return template('item_new', locals())
  
  @check_permission("create_group", "Can't create group")
  def create_group_post(self, request):
    form = GroupForm(data=request.POST)
    if form.is_valid():
      new_group = form.save(commit=False)
      new_group.create_user = get_current_user()
      new_group.put()
      # add itself as a member
      new_group.join(get_current_user())
      
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
    return site.view(self.request)

class SiteNewGroupHandler(SiteHandler):
  """docstring for SiteNewGroupHandler"""
  def get_impl(self, site):
    return site.create_group()
  
  def post_impl(self, site, request):
    return site.create_group_post(request)


apps = [(r'/group', SiteViewHandler),
        (r'/group/new', SiteNewGroupHandler),
        ]