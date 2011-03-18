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
  site_slogan = db.StringProperty(required=True, \
    default= _("Want to be the best open source SNS!"))
  
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
  user = db.ReferenceProperty(User, required=True)
  
  introduction = db.StringFlyProperty(default=1)
  
  comment_count = db.IntegerFlyProperty(default=1)
  stream_count = db.IntegerFlyProperty(default=1)
  follower_count = db.IntegerFlyProperty(default=1)
  following_count = db.IntegerFlyProperty(default=1)
  
  def can_view(self, user):
    """docstring for can_view"""
    # people always can view other's homepage
    return True
  
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
    
  def get_follower_keys(self):
    """docstring for get_follower_keys"""
    return User.get_source_keys(FOLLOW, self.user)
  
  def get_followers(self):
    """docstring for get_followers"""
    return db.MapQuery(self.get_following_keys(), lambda x: db.get(x), True)
  
  def get_following_keys(self):
    """docstring for get_folloing_keys"""
    return self.user.get_target_keys(FOLLOW)
  
  def get_following(self):
    """docstring for get_following"""
    return db.MapQuery(self.get_folloing_keys(), lambda x: db.get(x), True)
  
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
    stream.author_stream_info = self
    stream.author = self.user
    
    stream.put()
    
    stream.add_subscribers(self.get_follower_keys())
    
    stream.notify()
    
    self.update_stream_count()
  
  def delete_stream(self, stream):
    """docstring for delete_stream"""
    stream.undo_notify()
    
    stream.delete()
    
    self.update_stream_count()
  
  def get_latest_streams(self):
    """docstring for get_all_streams"""
    return UserStream.all(author_stream_info=author_stream_info)\
      .order("-create_at")
  
  ############
  #
  # User info update
  #
  ############
  
  def update_field(self, field, value):
    """docstring for update_data"""
    setattr(self, field, value)
    self.put()
  
  def update_stream_count(self):
    """docstring for update_comment_count"""
    count = UserStream.all(author_stream_info = self).count()
    self.update_field('stream_count', count)
  
  def update_follower_count(self):
    """docstring for update_follower_count"""
    count = User.get_source_keys(FOLLOW, self.user).count()
    self.update_field('follower_count', count)
  
  def update_following_count(self):
    """docstring for update_following_count"""
    count = self.user.get_target_keys(FOLLOW)
    self.update_field('following_count', count)
  
  @classmethod
  def get_instance(cls, user):
    """docstring for get_instance"""
    info = UserStreamInfo.all(user=user).get()
    if not info:
      info = UserStreamInfo(user=user)
      info.put()
    return info

class UserStream(gdb.Message):
  """docstring for UserStream"""
  author_stream_info = db.ReferenceProperty(UserStreamInfo)
  author = db.ReferenceProperty(User)
  
  action = db.StringFlyProperty(default='')
  content = db.StringFlyProperty(default='')
  
  def can_comment(self, user):
    """docstring for can_comment"""
    self.author_stream_info.has_follower(user)
  
  def create_comment(self, comment, user):
    """docstring for create_comment"""
    comment.stream = self
    comment.author = self.author
    
    comment.put()
  
  def delete_comment(self, comment, user):
    """docstring for delete_comment"""
    comment.delete()
    
  def get_all_comments(self):
    """docstring for get_all_comments"""
    return UserStreamComment.all(stream=self).order('create_at')

class UserStreamComment(gdb.Message):
  """docstring for UserStreamComment"""
  stream = db.ReferenceProperty(UserStream)
  author = db.ReferenceProperty(User)
  
  content = db.StringFlyProperty(default='')



