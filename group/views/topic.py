#!/usr/bin/env python
# encoding: utf-8
"""
topic.py

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

class TopicForm(djangoforms.ModelForm):
  """docstring for TopicForm"""
  class Meta:
    model = Topic

class TopicUI(PermissionUI):
  """docstring for TopicUI"""
  def __init__(self, topic):
    super(TopicUI, self).__init__(topic)
    self.topic = topic
  
  @view_method
  @check_permission('view', "Not allowed to open topic")
  def view(self):
    """docstring for view"""
    pass
  
  @view_method
  @check_permission('edit', "Not the author")
  def edit(self):
    """docstring for edit"""
    pass
  
  @check_permission('edit', "Not the author")
  def edit_post(self, request):
    """docstring for edit_post"""
    pass
  
  @view_method
  @check_permission('reply', "Not allowed to reply the thread")
  def create_post(self):
    """docstring for create_post"""
    pass
  
  @check_permission('reply', "Not allowed to reply the thread")
  def create_post_post(self, request):
    """docstring for create_post_post"""
    pass

class TopicHandler(webapp.RequestHandler):
  """docstring for TopicHandler"""
  @login_required
  @api_enabled
  def get(self, topic_id):
    """docstring for get"""
    topic = Topic.get_by_id(int(topic_id))
    return 'topic_display.html', locals()