#!/usr/bin/env python
# encoding: utf-8
"""
group.py

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""


import logging
import settings

from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms

from duser.auth import get_current_user
from api.webapp import login_required, api_enabled
from api.webapp import check_permission, view_method, PermissionUI

from group.models import *

class GroupForm(djangoforms.ModelForm):
  class Meta:
    model = Group
    fields = ['title', 'introduction']

class GroupUI(PermissionUI):
  """docstring for GroupUI"""
  def __init__(self, group):
    super(GroupUI, self).__init__(group)
    self.group = group
  
  @view_method
  @check_permission('view', "Not allowed to open the group")
  def view(self):
    """docstring for view"""
    return 'group_display.html', locals()
  
  @view_method
  @check_permission('edit', "Not a admin user")
  def edit(self):
    """docstring for edit"""
    pass
  
  @check_permission('edit', "Not a admin user")
  def edit_post(self, request):
    """the post_back handler for edit group info"""
    pass
        
  @view_method
  @check_permission('join', "Can't join group")
  def join(self):
    """docstring for join"""
    pass
  
  @check_permission('join', "Can't join group")
  def join_post(self, request):
    """docstring for join_post"""
    pass
  
  @view_method
  @check_permission('create_thread', "Not allowed to create thread here")
  def create_thread(self):
    """docstring for create_thread"""
    pass
    
  @check_permission('create_thread', "Not allowed to create thread here")
  def create_thread_post(self, request):
    """docstring for create_thread_post"""
    pass

class GroupHandler(webapp.RequestHandler):
  """docstring for GroupHandler"""
  def get_impl(self, groupui):
    """docstring for get_impl"""
    raise Exception("Have not implemented")
  
  def post_impl(self, groupui, request):
    """docstring for post_impl"""
    return self.get_impl(groupui)

  @api_enabled
  def get(self, group_id):
    """docstring for get"""
    group = Group.get_by_id(int(group_id))
    return self.get_impl(GroupUI(group))
  
  @api_enabled
  def post(self, group_id):
    """docstring for post"""
    group = Group.get_by_id(int(group_id))
    return self.post_impl(GroupUI(group), self.request)

class GroupViewHandler(GroupHandler):
  """docstring for GroupViewHandler"""
  def get_impl(self, groupui):
    """docstring for get_impl"""
    return groupui.view()

class GroupNewTopicHandler(GroupHandler):
  """docstring for GroupNewTopicHandler"""

class GroupEditHandler(GroupHandler):
  """docstring for GroupNewTopicHandler"""

class GroupJoinHandler(GroupHandler):
  """docstring for GroupNewTopicHandler"""


apps = [(r'/group/(\d+)', GroupViewHandler),
        (r'/group/(\d+)/new', GroupNewTopicHandler),
        (r'/group/(\d+)/join', GroupJoinHandler),
        (r'/group/(\d+)/edit', GroupEditHandler),
        ]
