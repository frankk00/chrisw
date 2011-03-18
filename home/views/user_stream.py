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

class UserStreamForm(djangoforms.ModelForm):
  """docstring for UserStreamForm"""
  class Meta:
    model = UserStream
    fields = ['content']
  
  content = fields.CharField(label=_('Content of stream'))

class UserStreamUI(ModelUI):
  """docstring for UserStreamUI"""
  def __init__(self, user_stream_info):
    super(UserStreamUI, self).__init__(user_stream_info)
    self.user_stream_info = user_stream_info
    self.user = user_stream_info.user
    
    self.current_user = get_current_user()
  
  def _home(self, request, new_vars={}):
    """docstring for _home"""
    
    limit = int(request.get('limit',20))
    offset = int(request.get('offset',0))
    
    groupinfo = UserGroupInfo.get_by_user(self.user)
    joined_groups = groupinfo.get_recent_joined_groups()
    
    is_login_user = self.user.key() == get_current_user().key()
    
    stream_form = UserStreamForm()
    
    query = UserStream.latest_by_author(self.user)
    
    page = Page(query=query, limit=limit, offset=offset, request=request)
    
    streams = page.data()
    
    for stream in streams:
      logging.debug("stream %s", stream)
    
    post_url = request.path
    
    
    var_dict = locals()
    var_dict.update(new_vars)
    
    return var_dict
  
  @check_permission('view', _("Can't visit given user's homepage"))
  def home(self, request):
    """docstring for home"""
    
    return template('user_home', self._home(request))
  
  @check_permission('create_stream', _("Can't create stream for user"))
  def home_post(self, request):
    """docstring for home_post"""

    stream_form = UserStreamForm(data=request.POST)
    
    if stream_form.is_valid():
      new_stream = stream_form.save(commit=False)
      self.user_stream_info.create_stream(new_stream)

    return template('user_home', self._home(request, locals()))
    
class UserStreamHandler(handlers.RequestHandler):
  """docstring for UserStreamHandler"""
  
  def get_impl(self, user_stream_ui):
    """docstring for get_impl"""
    raise Exception("Not implemented")
  
  def post_impl(self, user_stream_ui):
    """docstring for post_impl"""
    return self.get_impl(user_stream_ui)
  
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
  
  def post_impl(self, user_stream_ui):
    """docstring for post_impl"""
    return user_stream_ui.home_post(self.request)

apps = [(r'/u/(\d+)', UserStreamHomeHandler)]
