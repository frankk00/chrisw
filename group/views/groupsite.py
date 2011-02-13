#!/usr/bin/env python
# encoding: utf-8
"""
group_site.py

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

from google.appengine.ext import webapp, db
from google.appengine.ext.db import djangoforms

from duser.auth import get_current_user, Guest
from api.webapp import *
from group.models import *
from groupui import GroupForm
from conf import settings

class GroupSiteUI(PermissionUI):
  """docstring for GroupSiteUI"""
  def __init__(self, group_site):
    super(GroupSiteUI, self).__init__(group_site)
    self.group_site = group_site
    self.user = get_current_user()
    self.groupinfo = UserGroupInfo.get_by_user(self.user)
    
  @view_method
  def view(self, request):
    offset = int(request.get("offset", "0"))
    limit = int(request.get("limit", "20"))
    
    my_groups = []
    
    if self.groupinfo:
      # user
      my_groups = db.get(self.groupinfo.groups)
    
    recommend_groups = [g for g in Group.all().fetch(10) \
      if g.key() not in self.groupinfo.groups]
    
    topic_groups = my_groups
    if self.user == Guest:
      topic_groups = recommend_groups
    
    topics = Topic.all().filter("group IN", topic_groups)\
      .order("-update_time").fetch(20)
    
    logging.debug("Fetched recent topics" + str(topics))
    
    # count the topics etc
    topic_count = Topic.all().filter("author =", self.user).count()
    post_count = Post.all().filter("author =", self.user).count()
    group_count = len(my_groups)
    
    display_group_name = True
    
    return template('groupsite_display.html', locals())
  
  @view_method
  @check_permission("create_group", "Can't create group")
  def create_group(self):
    form = GroupForm()
    post_url = '/group/new'
    return template('item_new', locals())
  
  @view_method
  @check_permission("create_group", "Can't create group")
  def create_group_post(self, request):
    form = GroupForm(data=request.POST)
    if form.is_valid():
      new_group = form.save(commit=False)
      new_group.create_user = get_current_user()
      new_group.put()
      # add itself as a member
      new_group.join(get_current_user())
      # add new group to site
      self.group_site.add_group(new_group)
      
      return redirect('/group/%d' % new_group.key().id())
    return template('item_new', locals())

class GroupSiteHandler(webapp.RequestHandler):
  """docstring for SiteHandler"""
  
  def get_impl(self, group_site):
    raise Exception("Have not implemented")
  
  def post_impl(self, group_site, request):
    return self.get_impl(group_site)
  
  @api_enabled
  def get(self):
    return self.get_impl(GroupSiteUI(GroupSite.get_instance()))
  
  @api_enabled
  def post(self):
    return self.post_impl(GroupSiteUI(GroupSite.get_instance()), self.request)
    
class GroupSiteViewHandler(GroupSiteHandler):
  """docstring for SiteViewHandler"""
  def get_impl(self, group_site):
    return group_site.view(self.request)

class GroupSiteNewGroupHandler(GroupSiteHandler):
  """docstring for SiteNewGroupHandler"""
  def get_impl(self, group_site):
    return group_site.create_group()
  
  def post_impl(self, group_site, request):
    return group_site.create_group_post(request)


apps = [(r'/group', GroupSiteViewHandler),
        (r'/group/new', GroupSiteNewGroupHandler),
        ]