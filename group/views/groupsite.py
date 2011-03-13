#!/usr/bin/env python
# encoding: utf-8
"""
group_site.py

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

from chrisw.core import handlers
from chrisw.core.action import *
from chrisw.core.ui import ModelUI, check_permission
from chrisw.i18n import _
from chrisw.helper import Page, djangoforms
from chrisw.helper.django_helper import fields, forms

from duser.auth import get_current_user, Guest
from group.models import *
from groupui import GroupForm
from conf import settings

class GroupSiteUI(ModelUI):
  """docstring for GroupSiteUI"""
  def __init__(self, group_site):
    super(GroupSiteUI, self).__init__(group_site)
    self.group_site = group_site
    self.user = get_current_user()
    self.group_info = UserGroupInfo.get_by_user(self.user)
    
  def view(self, request):
    offset = int(request.get("offset", "0"))
    limit = int(request.get("limit", "20"))
    
    group_info = self.group_info
    
    my_groups = group_info.get_recent_joined_groups()
    
    query = GroupTopic.latest_by_subscriber(self.user)
    count = query.count(200)
    topics = query.fetch(limit, offset)
    
    page = Page(count=count, offset=offset, limit=limit, request=request)
    
    logging.debug("Fetched recent topics" + str(topics))
    
    sidebar_widgets = [forward('/group/recommend').render()]
    
    display_group_name = True
    
    return template('groupsite_display.html', locals())
  
  def recommend_groups(self):
    """docstring for recommend_groups"""
    
    recommend_groups = [g for g in Group.all().fetch(10)]
    
    return template('window_recommend_groups', locals())
  
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
      self.group_site.add_group(new_group, self.user)
      
      return redirect('/group/%d' % new_group.key().id())
    return template('item_new', locals())

class GroupSiteHandler(handlers.RequestHandler):
  """docstring for SiteHandler"""
  
  def get_impl(self, group_site):
    raise Exception("Have not implemented")
  
  def post_impl(self, group_site, request):
    return self.get_impl(group_site)
  
  def get(self):
    return self.get_impl(GroupSiteUI(GroupSite.get_instance()))
  
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

class GroupSiteRecommandGroupsHandler(GroupSiteHandler):
  """docstring for GroupSiteRecommandGroupsHandler"""
  def get_impl(self, group_site):
    """docstring for get_impl"""
    return group_site.recommend_groups()


apps = [(r'/group', GroupSiteViewHandler),
        (r'/group/new', GroupSiteNewGroupHandler),
        (r'/group/recommend', GroupSiteRecommandGroupsHandler)
        ]