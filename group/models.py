#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-25.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from google.appengine.api import users

from api import db
from duser import User, Guest
from conf import settings

class Site(db.Model):
  """a faked object"""
  def get_groups(self):
    """docstring for get_groups"""
    pass
  
  def can_create_group(self, user):
    return True
  
  @classmethod
  def get_instance(cls):
    """docstring for get_instance"""
    instance = super(Site, cls).all().get()
    if not instance:
      instance = Site()
      instance.put()
      
    return instance

class UserGroupInfo(db.Model):
  """docstring for UserGroupProfile"""
  user = db.ReferenceProperty(required=True)
  # stored group using keys
  groups = db.ListProperty(db.Key,required=True, default=[])
  
  @classmethod
  def get_by_user(self, user):
    """docstring for get_by_user"""
    # init all needed object here
    if user != Guest:
      groupinfo = UserGroupInfo.all().filter("user =", user).get()
      if not groupinfo:
        groupinfo = UserGroupInfo(user=user)
        groupinfo.put()
    
    else: groupinfo = None
    return groupinfo

class Group(db.Model):
  """docstring for Board"""
  create_time = db.DateTimeProperty(auto_now_add=True)
  title = db.StringProperty()
  introduction = db.TextProperty()
  create_user = db.ReferenceProperty(User)
  admin_users = db.ListProperty(db.Key,required=True, default=[])
  members = db.ListProperty(db.Key,required=True, default=[])
  photo_url = db.StringProperty(default=settings.DEFAULT_GROUP_PHOTO)
    
  def can_view(self, user):
    """docstring for can_see"""
    return True
    
  def can_edit(self, user):
    """docstring for can_edit"""
    return True
  
  def can_delete(self):
    """docstring for can_delete"""
    return True
  
  def can_create_topic(self, user):
    """docstring for can_create_thread"""
    return True
  
  def can_join(self, user):
    """docstring for can_join"""
    return not user.key() in self.members
  
  def join(self, user):
    userinfo = UserGroupInfo.get_by_user(user)
    userinfo.groups.append(self.key())
    self.members.append(userinfo.user.key())
    userinfo.put()
    self.put()
    
  def quit(self, user):
    """docstring for quit"""
    userinfo = UserGroupInfo.get_by_user(user)
    userinfo.groups.remove(self.key())
    self.members.remove(user.key())
    userinfo.put()
    self.put()
    
  def can_quit(self, user):
    """docstring for can_quit"""
    return user.key() in self.members and user.key() != self.create_user.key()
  
  def get_topics(self):
    """docstring for get_topics"""
    return Topic.all().filter("group =", self).order("-update_time")
  

class Topic(db.Model):
  """docstring for Thread"""
  create_time = db.DateTimeProperty(auto_now_add=True)
  update_time = db.DateTimeProperty(auto_now_add=True)
  author = db.ReferenceProperty(User)
  title = db.TextProperty()
  content = db.TextProperty()
  group = db.ReferenceProperty(Group)
  length = db.IntegerProperty(default=1)
  
  def can_view(self, user):
    """docstring for can_view"""
    return self.group.can_view(user)
  
  def can_edit(self, user):
    """docstring for can_edit"""
    return user.username == self.author.username
  
  def can_reply(self, user):
    """docstring for can_create_thread"""
    from duser.auth import Guest
    return self.can_view(user) and user != Guest
  
  def can_delete(self):
    """docstring for can_delete"""
    return True
  
  def get_posts(self):
    """docstring for get_posts"""
    return Post.all().filter("topic =", self).order("create_time")
  
class Post(db.Model):
  """docstring for Post"""
  create_time = db.DateTimeProperty(auto_now_add=True) 
  author = db.ReferenceProperty(User)
  topic = db.ReferenceProperty(Topic)
  content = db.TextProperty()

