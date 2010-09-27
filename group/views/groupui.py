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
from api.webapp import *
from group.models import *
from topic import TopicForm

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
    return template('group_display.html', locals())
  
  @view_method
  @check_permission('edit', "Not a admin user")
  def edit(self):
    """docstring for edit"""
    form = GroupForm(data=self.group.to_dict())
    post_url = '/group/%d/edit' % self.group.key().id()
    return template('item_new', locals())
  
  @check_permission('edit', "Not a admin user")
  def edit_post(self, request):
    """the post_back handler for edit group info"""
    form = GroupForm(data=request.POST, instance=self.group)
    if form.is_valid():
      new_group = form.save(commit=False)
      new_group.put()
      return redirect('/group/%d' % self.group.key().id())
    return template('item_new', locals())
        
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
  @check_permission('create_topic', "Not allowed to create topic here")
  def create_topic(self):
    """docstring for create_topic"""
    pass
    
  @check_permission('create_topic', "Not allowed to create topic here")
  def create_topic_post(self, request):
    """docstring for create_topic_post"""
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
  def get_impl(self, groupui):
    return groupui.create_topic()
  
  def post_impl(self, groupui, request):
    return groupui.create_topic_post(request)

class GroupEditHandler(GroupHandler):
  """docstring for GroupNewTopicHandler"""
  def get_impl(self, groupui):
    return groupui.edit()
    
  def post_impl(self, groupui, request):
    return groupui.edit_post(request)

class GroupJoinHandler(GroupHandler):
  """docstring for GroupNewTopicHandler"""
  def get_impl(self, groupui):
    return groupui.join()
  
  def post_impl(self, groupui, request):
    return groupui.join_post(request)

apps = [(r'/group/(\d+)', GroupViewHandler),
        (r'/group/(\d+)/new', GroupNewTopicHandler),
        (r'/group/(\d+)/join', GroupJoinHandler),
        (r'/group/(\d+)/edit', GroupEditHandler),
        ]
