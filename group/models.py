#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-25.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from google.appengine.api import users

from chrisw import db

from common import models as ndb
from duser import User, Guest
from conf import settings


GROUP_MEMEBERSHIP = 'has-group-member'
GROUP_ADMIN = 'has-group-admin'

class GroupSite(db.Model):
  """a faked object"""
  
  avaliable_group_slots = db.IntegerProperty(required=True, default=100)
  
  def get_groups(self):
    """docstring for get_groups"""
    pass
  
  def add_group(self, group):
    """docstring for add_group"""
    self.avaliable_group_slots -= 1
    self.put()
  
  def can_create_group(self, user):
    return self.avaliable_group_slots > 0
  
  @classmethod
  def get_instance(cls):
    """docstring for get_instance"""
    instance = super(GroupSite, cls).all().get()
    if not instance:
      instance = GroupSite()
      instance.put()
      
    return instance

class UserGroupInfo(ndb.Entity):
  """docstring for UserGroupProfile"""
  user = db.ReferenceProperty(required=True)
  # stored group using keys
  
  @classmethod
  def get_by_user(self, user):
    """docstring for get_by_user"""
    # init all needed object here
    groupinfo = UserGroupInfo.all().filter("user =", user).get()
    if not groupinfo:
      groupinfo = UserGroupInfo(user=user)
      groupinfo.put()
    return groupinfo

class Group(ndb.Entity):
  """docstring for Board"""
  create_time = db.DateTimeProperty(auto_now_add=True)
  create_user = db.ReferenceProperty(User)
  
  title = db.StringFlyProperty()
  introduction = db.TextFlyProperty()
  photo_url = db.StringFlyProperty(default=settings.DEFAULT_GROUP_PHOTO)
  recent_members = db.ListFlyProperty()
    
  def can_view(self, user):
    """docstring for can_see"""
    return True
    
  def can_edit(self, user):
    """docstring for can_edit"""
    return user.key() == self.create_user.key() or user.key() in self.admin_users
  
  def can_delete(self):
    """docstring for can_delete"""
    return user.key() == self.create_user.key()

  #######
  #
  # membership related apis
  #
  #######
  
  def can_join(self, user):
    """docstring for can_join"""
    return user != Guest and (not user.key() in self.members)

  def can_quit(self, user):
    """docstring for can_quit"""
    return user.key() in self.members and user.key() != self.create_user.key()
  
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
  
  def has_member(self, user):
    """docstring for has_member"""
    pass
  
  def get_latest_joined_members(self):
    """docstring for get_latest_joined_members"""
    pass
  
  def get_members(self, limit=24):
    """docstring for get_members"""
    pass
  
  #######
  #
  # admin related apis
  #
  #######
  def can_edit_admin(self):
    """docstring for can_add_admin"""
    pass
  
  def add_admin(self, new_admin):
    """docstring for add_admin"""
    pass
  
  def remove_admin(self, new_admin):
    """docstring for remove_admin"""
    pass
  
  def has_admin(self, user):
    """docstring for has_admin"""
    pass
  
  def get_admins(self, limit=24):
    """docstring for get_admins"""
    pass
  

  def can_create_topic(self, user):
    """docstring for can_create_thread"""
    return user.key() in self.members  
  
  def can_delete_topic(self):
    """docstring for can_delete_topic"""
    pass
  
  def create_topic(self, topic):
    """docstring for create_topic"""
    pass
  
  def delete_topic(self, topic):
    """docstring for delete_topic"""
    pass
  
  def get_topics(self):
    """docstring for get_topics"""
    return Topic.all().filter("group =", self).order("-update_time")
  

class GroupTopic(ndb.Message):
  """docstring for Thread"""
  update_at = db.DateTimeProperty(auto_now=True)
  author = db.ReferenceProperty(User)
  group = db.ReferenceProperty(Group)
  
  title = db.FlyTextProperty()
  content = db.FlyTextProperty()
  length = db.FlyIntegerProperty(default=1)
  hits = db.FlyIntegerProperty(default=0)
  
  def can_view(self, user):
    """docstring for can_view"""
    return self.group.can_view(user)
  
  def can_edit(self, user):
    """docstring for can_edit"""
    return user.key() == self.author.key()

  def can_delete(self, user):
    """docstring for can_delete"""
    return self.author.key() == user.key()

  #######
  #
  # post related apis
  #
  #######

  def can_create_post(self, user):
    """docstring for can_create_thread"""
    from duser.auth import Guest
    return self.can_view(user) and user != Guest
  
  def can_delete_post(self, user):
    """docstring for can_delete_post"""
    pass
  
  def create_post(self, post):
    """docstring for add_group_post"""
    pass

  def delete_post(self, post):
    """docstring for delete_post"""
    pass
  
  def get_posts(self):
    """docstring for get_posts"""
    return Post.all().filter("topic =", self).order("create_time")
  
class GroupPost(ndb.Message):
  """docstring for Post"""
  author = db.ReferenceProperty(User)
  topic = db.ReferenceProperty(Topic)
  content = db.TextFlyProperty()
