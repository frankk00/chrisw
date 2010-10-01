#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-25.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from google.appengine.api import users

from api import db
from duser import User

class Site(db.Model):
  """a faked object"""
  def get_groups(self):
    """docstring for get_groups"""
    pass
  
  def can_create_group(self, user):
    return True
  

class UserGroupInfo(db.Model):
  """docstring for UserGroupProfile"""
  user_id = db.IntegerProperty(required=True)
  # stored group using keys
  group_ids = db.ListProperty(int,required=True, default=[])

class Group(db.Model):
  """docstring for Board"""
  create_time = db.DateTimeProperty(auto_now_add=True)
  title = db.StringProperty()
  introduction = db.TextProperty()
  create_user = db.ReferenceProperty(User)
  admin_user_ids = db.ListProperty(int,required=True, default=[])
  member_ids = db.ListProperty(int,required=True, default=[])
    
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
    return not user.key().id() in self.member_ids
  
  def join(self, user):
    userinfo = UserGroupInfo.all().filter("user_id =", user.key().id()).get()
    userinfo.group_ids.append(self.key().id())
    self.member_ids.append(userinfo.user_id)
    userinfo.put()
    self.put()
    
  def quit(self, user):
    """docstring for quit"""
    pass
    
  def can_quit(self, user):
    """docstring for can_quit"""
    return user.key().id() in self.member_ids and user.key().id() != self.create_user.key().id()
  
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
  
  def can_view(self, user):
    """docstring for can_view"""
    return self.group.can_view(user)
  
  def can_edit(self, user):
    """docstring for can_edit"""
    return user.username == author.username
  
  def can_reply(self, user):
    """docstring for can_create_thread"""
    return self.can_view(user)
  
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

