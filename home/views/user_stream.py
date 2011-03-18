#!/usr/bin/env python
# encoding: utf-8
"""
user_stream.py

Created by Kang Zhang on 2011-03-18.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


import logging

from chrisw.core import handlers
from chrisw.core.action import *
from chrisw.core.ui import ModelUI, check_permission
from chrisw.core.memcache import cache_action
from chrisw.i18n import _
from chrisw.helper import Page, djangoforms
from chrisw.helper.django_helper import fields, forms

from common.auth import get_current_user
from common.models import User
from conf import settings

from group.models import *
from home.models import *



class UserStreamUI(ModelUI):
  """docstring for UserStreamUI"""
  def __init__(self, user_stream_info):
    super(UserStreamUI, self).__init__(user_stream_info)
    self.user_stream_info = user_stream_info
    self.user = user_stream_info.user
    
    self.current_user = get_current_user()
  
  @check_permission('view', _("Can't visit given user's homepage"))
  def home(self, request):
    """docstring for home"""
    
    groupinfo = UserGroupInfo.get_by_user(self.user)
    joined_groups = groupinfo.get_recent_joined_groups()
    
    is_login_user = self.user.key() == get_current_user().key()
    
    return template('user_home', locals())
    
class UserStreamHandler(handlers.RequestHandler):
  """docstring for UserStreamHandler"""
  
  def get_impl(self, user_stream_ui):
    """docstring for get_impl"""
    raise Exception("Not implemented")
  
  def post_impl(self, user_stream_ui):
    """docstring for post_impl"""
    return self.get_impl(self. user_stream_ui)
  
  def get(self, user_id):
    """docstring for get"""
    user = User.get_by_id(int(user_id))
    user_stream_info = UserStreamInfo.get_instance(user=user)
    return self.get_impl(UserStreamUI(user_stream_info))
  
  def post(self, user_id):
    """docstring for post"""
    user = User.get_by_id(int(user_id))
    user_stream_info = UserStreamInfo.get_instance(user=user)
    return self.post_impl(UserStreamUI(user_stream_info))

class UserStreamHomeHandler(UserStreamHandler):
  
  def get_impl(self, user_stream_ui):
    """docstring for get_impl"""
    return user_stream_ui.home(self.request)

apps = [(r'/u/(\d+)', UserStreamHomeHandler)]
