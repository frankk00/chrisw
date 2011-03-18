#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw import db, gdb
from chrisw.i18n import _
from chrisw.core.memcache import cache_result

from common.auth import User

FOLLOW = 'user-follow'

class Site(db.Model):
  """a faked object"""
  site_name = db.StringProperty(required=True, default= _("Daoshicha.com"))
  site_slogan = db.StringProperty(required=True, default= _("Want to be the best open source SNS!"))
  
  @classmethod
  @cache_result('global-site', 240)
  def get_instance(cls):
    """docstring for get_instance"""
    instance = super(Site, cls).all().get()
    if not instance:
      instance = Site()
      instance.put()
      
    return instance

class UserSite(db.Model):
  """A faked object for the user management"""
  
  @classmethod
  @cache_result('usersite-instance', 240)
  def get_instance(cls):
    """docstring for get_instance"""
    instance = super(UserSite, cls).all().get()
    if not instance:
      instance = UserSite()
      instance.put()
      
    return instance
  

class Photo(db.Model):
  """docstring for ProfilePhoto"""
  blob_key = db.StringProperty()
  url = db.StringProperty()
  
class UserStreamInfo(gdb.Entity):
  """docstring for UserStreamInfo"""
  user = db.ReferenceProperty(User)
  
  comment_count = db.IntegerFlyProperty(default=1)
  stream_count = db.IntegerFlyProperty(default=1)
  follower_count = db.IntegerFlyProperty(default=1)
  following_count = db.IntegerFlyProperty(default=1)
  
  def can_follow(self, user):
    """docstring for can_follow"""
    return not self.has_follower(user) and not self.is_me(user)
  
  def follow(self, user):
    """docstring for follow"""
    self.user.link(FOLLOW, user)
  
  def unfollow(self, user):
    """docstring for unfollow"""
    self.user.unlink(FOLLOW, user)
  
  def has_follower(self, user):
    """docstring for has_follower"""
    self.user.has_link(FOLLOW, user)
  
  def is_me(self, user):
    """docstring for is_me"""
    return user.key() == self.user.key()
  
  ############
  #
  # Stream related apis
  #
  ############
  
  def can_create_stream(self, user):
    """docstring for can_create_stream"""
    return self.is_me(user)
  
  def create_stream(self, stream):
    """docstring for create_stream"""
    pass
  
  def delete_stream(self, stream):
    """docstring for delete_stream"""
    pass
  
  def get_all_streams(self):
    """docstring for get_all_streams"""
    pass
  
  
  @classmethod
  def get_instance(cls, user):
    """docstring for get_instance"""
    return UserStreamInfo.all(user=user).get()

class UserStream(gdb.Message):
  """docstring for UserStream"""
  author = db.ReferenceProperty(User)
  action = db.StringFlyProperty(default='')
  content = db.StringFlyProperty(default='')

class UserStreamComment(UserStream):
  """docstring for UserStreamComment"""
  stream = db.ReferenceProperty(UserStream)




