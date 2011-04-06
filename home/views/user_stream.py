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
from common.models import User, Guest
from conf import settings

from group.models import *
from home.models import *

class UserStreamForm(djangoforms.ModelForm):
  """docstring for UserStreamForm"""
  class Meta:
    model = UserStream
    fields = ['content']
  
  content = fields.CharField(label=_('Content of stream'), max_length=140)

class UserStreamUI(ModelUI):
  """docstring for UserStreamUI"""
  def __init__(self, user_stream_info):
    super(UserStreamUI, self).__init__(user_stream_info)
    self.user_stream_info = user_stream_info
    self.user = user_stream_info.user
    
    self.current_user = get_current_user()
  
  def _home(self, query, request, new_vars={}):
    """docstring for _home"""
    
    limit = int(request.get('limit',20))
    offset = int(request.get('offset',0))
    
    groupinfo = UserGroupInfo.get_by_user(self.user)
    joined_groups = groupinfo.get_recent_joined_groups()
    
    stream_form = UserStreamForm()
    
    page = Page(query=query, limit=limit, offset=offset, request=request)
    
    streams = page.data()
    
    following_users = self.user_stream_info.recent_following_users()
    follower_users = self.user_stream_info.recent_follower_users()
    
    for stream in streams:
      logging.debug("stream %s", stream)
    
    post_url = "/u/%d" % self.user.key().id()
    
    var_dict = locals()
    var_dict.update(new_vars)
    
    return var_dict

  def home(self, request):
    """docstring for home"""
    if self.user_stream_info.can_view_following(self.current_user):
      return redirect("/u/%d/following" % self.user.key().id())
    return redirect("/u/%d/all" % self.user.key().id())
  
  @check_permission('view_all', _("Can't visit given user's homepage"))
  def home_all(self, request):
    """docstring for home"""
    query = UserStream.latest_by_author(self.user)
    return template('page_user_stream_view_all', self._home(query, request))

  @check_permission('view_following', _("Can't visit given user's homepage"))
  def home_following(self, request):
    """docstring for home_following"""
    query = UserStream.latest_by_subscriber(self.user)
    return template('page_user_stream_view_following', self._home(query, request))
  
  @check_permission('create_stream', _("Can't create stream for user"))
  def home_post(self, request):
    """docstring for home_post"""

    stream_form = UserStreamForm(data=request.POST)
    
    if stream_form.is_valid():
      new_stream = stream_form.save(commit=False)
      self.user_stream_info.create_stream(new_stream)

    return back()
  
  @check_permission('follow', _("Can't follow the user"))
  def follow(self):
    """docstring for follow"""
    self.user_stream_info.follow(self.current_user)
    return back()
  
  @check_permission('unfollow', _("Can't unfollow given user"))
  def unfollow(self):
    """docstring for unfollow"""
    self.user_stream_info.unfollow(self.current_user)
    return back()
    
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

class UserStreamHomeAllHandler(UserStreamHandler):
  """docstring for UserStreamHomeAllHandler"""
  def get_impl(self, user_stream_ui):
    """docstring for get_impl"""
    return user_stream_ui.home_all(self.request)
  
class UserStreamHomeFollowingHandler(UserStreamHandler):
  """docstring for UserStreamHomeAllHandler"""
  def get_impl(self, user_stream_ui):
    """docstring for get_impl"""
    return user_stream_ui.home_following(self.request)

class UserStreamHomeFollowHandler(UserStreamHandler):
  """docstring for UserStreamHomeFollowHandler"""
  def get_impl(self, user_stream_ui):
    """docstring for get_impl"""
    return user_stream_ui.follow()
  
class UserStreamHomeUnfollowHandler(UserStreamHandler):
  """docstring for UserStreamHomeUnfollowHandler"""
  def get_impl(self, user_stream_ui):
    """docstring for get_impl"""
    return user_stream_ui.unfollow()

class UserStreamHomeRootHandler(handlers.RequestHandler):
  """docstring for UserStreamHomeRootHandler"""
  def get(self):
    """docstring for get_impl"""
    user = get_current_user()
    if user.key() == Guest.key():
      return redirect(settings.DEFAULT_HOME)
    return redirect('/u/%d' % user.key().id())
          

apps = [(r'/u', UserStreamHomeRootHandler),
        (r'/u/(\d+)', UserStreamHomeHandler),
        (r'/u/(\d+)/all', UserStreamHomeAllHandler),
        (r'/u/(\d+)/following', UserStreamHomeFollowingHandler),
        (r'/u/(\d+)/follow', UserStreamHomeFollowHandler),
        (r'/u/(\d+)/unfollow', UserStreamHomeUnfollowHandler)]
