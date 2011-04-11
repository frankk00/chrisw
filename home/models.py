#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import re

from chrisw import db, gdb
from chrisw.i18n import _
from chrisw.core.memcache import cache_result

from common.auth import User, Guest

FOLLOWED_BY = 'user-followed-by'
TEXT_STREAM = 'text'

_VALID_NICK_ = r'[^ \s:@]+'
_KEY_FORMAT_ = r'%s' + _VALID_NICK_

_KEY_PATTERNS_ = (re.compile(_KEY_FORMAT_ % '@'),
                 re.compile(_KEY_FORMAT_ % '#'))

class Site(db.Model):
  """a faked object"""
  site_name = db.StringProperty(required=True, default= _("Daoshicha.com"))
  site_slogan = db.StringProperty(required=True, \
    default= _("Want to be the best open source SNS!"))
  
  @classmethod
  @cache_result('globalsite-instance', 240)
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
  
  recent_follower_keys = db.ListFlyProperty(default=[])
  recent_following_keys = db.ListFlyProperty(default=[])
  
  comment_count = db.IntegerFlyProperty(default=1)
  stream_count = db.IntegerFlyProperty(default=1)
  follower_count = db.IntegerFlyProperty(default=1)
  following_count = db.IntegerFlyProperty(default=1)
  
  def can_view_all(self, user):
    """docstring for can_view"""
    # people always can view other's homepage
    return True
  
  def can_view_following(self, user):
    """docstring for can_view_following"""
    return self.is_me(user)
  
  def can_view_mention(self, user):
    """docstring for can_view_mention"""
    return True
  
  def can_follow(self, user):
    """docstring for can_follow"""
    return not user is Guest and not self.has_follower(user) and not self.is_me(user)
  
  def can_unfollow(self, user):
    """docstring for can_unfollow"""
    return self.has_follower(user) and not self.is_me(user)
  
  def follow(self, user):
    """docstring for follow"""
    self.user.link(FOLLOWED_BY, user)
    
    self.update_follower_count()
    
    UserStreamInfo.get_instance(user).update_following_count()
  
  def unfollow(self, user):
    """docstring for unfollow"""
    self.user.unlink(FOLLOWED_BY, user)
    
    self.update_follower_count()
    
    UserStreamInfo.get_instance(user).update_following_count()
  
  def has_follower(self, user):
    """docstring for has_follower"""
    return self.user.has_link(FOLLOWED_BY, user)
    
  def get_following_keys(self):
    """docstring for get_follower_keys"""
    return User.get_sources(FOLLOWED_BY, self.user, keys_only=True)
  
  def get_followers(self):
    """docstring for get_followers"""
    return db.MapQuery(self.get_following_keys(), lambda x: db.get(x), True)
  
  def get_follower_keys(self):
    """docstring for get_following_keys"""
    return self.user.get_targets(FOLLOWED_BY, User, keys_only=True)
  
  def get_following(self):
    """docstring for get_following"""
    return db.MapQuery(self.get_following_keys(), lambda x: db.get(x), True)
  
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
    stream.init_keywords()
    
    stream.put()
    
    stream.notify(list(self.get_follower_keys()) + [self.user.key()])
    
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
    query = self.get_follower_keys();
    self.recent_follower_keys = list(query.fetch(10))
    self.update_field('follower_count', query.count())
  
  def update_following_count(self):
    """docstring for update_following_count"""
    query = self.get_following_keys()
    self.recent_following_keys = list(query.fetch(10))
    self.update_field('following_count', query.count())
  
  def recent_follower_users(self):
    """docstring for recent_follower_users"""
    return db.get(self.recent_follower_keys)
  
  def recent_following_users(self):
    """docstring for recent_following_users"""
    return db.get(self.recent_following_keys)
  
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
  author_stream_info = db.ReferenceProperty(UserStreamInfo, \
    collection_name = 'user_streams')
  author = db.ReferenceProperty(User, \
    collection_name = 'user_streams')
    
  target = db.ReferenceProperty()
  target_type = db.StringProperty(required=True, default=TEXT_STREAM)
  
  content = db.StringFlyProperty(default='')
  
  keywords = db.StringListProperty(required=True, default=[])
  
  def __init__(self, *args, **kwargs):
    """docstring for __init__"""
    
    for attr in ('target',):
      if kwargs.has_key(attr) and kwargs.get(attr):
        kwargs[attr + '_type'] = gdb._get_type_name(kwargs.get(attr))
    
    super(UserStream, self).__init__(*args, **kwargs)
    
  def init_keywords(self):
    """docstring for _init_keywords"""
    # init keywords index
    
    if self.content:
      for pattern in _KEY_PATTERNS_:
        for keyword in pattern.findall(self.content):
          self.keywords.append(keyword)
  
  def can_comment(self, user):
    """docstring for can_comment"""
    self.author_stream_info.has_follower(user)
  
  def create_comment(self, comment, user):
    """docstring for create_comment"""
    comment.stream = self
    comment.author = self.author
    
    comment.put()
    
    self.redo_notify()
  
  def delete_comment(self, comment, user):
    """docstring for delete_comment"""
    comment.delete()
    
  def get_all_comments(self):
    """docstring for get_all_comments"""
    return UserStreamComment.all(stream=self).order('create_at')
  
  @classmethod
  def latest_by_author(cls, author):
    """docstring for latest_by_author"""
    return cls.all(author=author).order('-create_at')
  
  @classmethod
  def latest_by_keyword(cls, keyword):
    """docstring for latest_by_keywords"""
    return cls.latest().filter('keywords', keyword)

class UserStreamComment(gdb.Message):
  """docstring for UserStreamComment"""
  stream = db.ReferenceProperty(UserStream)
  author = db.ReferenceProperty(User)
  
  content = db.StringFlyProperty(default='')



