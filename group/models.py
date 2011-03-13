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
RECENT_MEMBER_LIMIT = 20

class GroupSite(db.Model):
  """a faked object"""
  
  avaliable_group_slots = db.IntegerProperty(required=True, default=100)
  
  def get_groups(self):
    """docstring for get_groups"""
    pass
  
  def add_group(self, group, user):
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
  creator = db.ReferenceProperty(User)
  
  title = db.StringFlyProperty()
  introduction = db.TextFlyProperty()
  photo_url = db.StringFlyProperty(default=settings.DEFAULT_GROUP_PHOTO)
  recent_members = db.ListFlyProperty()
    
  def can_view(self, user):
    """docstring for can_see"""
    return True
      
  def can_delete(self, user):
    """docstring for can_delete"""
    return self.has_creator(user)
  
  def has_creator(self, user):
    """docstring for has_creator"""
    return user.key() == self.creator.key()

  #######
  #
  # membership related apis
  #
  #######
  
  def can_join(self, user):
    """docstring for can_join"""
    return user != Guest and (not self.has_member(user))

  def can_quit(self, user):
    """docstring for can_quit"""
    return self.has_member(user) and not self.has_creator(user)
  
  def join(self, user):
    self.create_relation(GROUP_MEMEBERSHIP, user)
    
    # add user to recent added users list
    self.recent_members.append(user.key())
    self.recent_members = self.recent_members[:RECENT_MEMBER_LIMIT]
    
    self.put()
    
  def quit(self, user):
    """docstring for quit"""
    self.delete_relation(GROUP_MEMEBERSHIP, user)
    
  def has_member(self, user):
    """docstring for has_member"""
    self.has_relation(GROUP_MEMEBERSHIP, user)
  
  def get_latest_joined_members(self):
    """docstring for get_latest_joined_members"""
    return db.get(self.recent_members.reverse())
  
  def get_member_keys(self, limit=24, offset=0):
    """docstring for get_members"""
    return self.get_target_keys(GROUP_MEMEBERSHIP, User, limit=limit, \
      offset=offset)
  
  def get_members(self, limit=24, offset=0):
    """docstring for get_members"""
    return db.get(self.get_member_keys(limit=limit, offset=offset))
  
  #######
  #
  # admin related apis
  #
  #######
  
  def can_edit(self, user):
    """If the user could edit the group"""
    return self.has_admin(user)
  
  def can_add_admin(self, user):
    """docstring for can_add_admin"""
    return self.has_creator(user)
  
  def can_remove_admin(self, user):
    """docstring for can_remove_admin"""
    return self.has_creator(user)
  
  def add_admin(self, new_admin):
    """docstring for add_admin"""
    return self.create_relation(GROUP_ADMIN, new_admin)
  
  def remove_admin(self, new_admin):
    """docstring for remove_admin"""
    return self.delete_relation(GROUP_ADMIN, new_admin)
  
  def has_admin(self, user):
    """docstring for has_admin"""
    return self.has_relation(GROUP_ADMIN, user)
  
  def get_admin_keys(self, limit=24, offset=0):
    """docstring for get_admins"""
    return self.get_target_keys(GROUP_ADMIN, User, limit=limit,\
      offset=offset)
  
  def get_admins(self, limit=24, offset=0):
    """docstring for get_admins"""
    return db.get(self.get_admin_keys(self, limit=limit, offset=offset))

  def can_create_topic(self, user):
    """docstring for can_create_thread"""
    return user.key() in self.members  

  #######
  #
  # topic related apis
  #
  #######
  
  def create_topic(self, topic, user):
    """ Create a new topi in group
    TODO: remove the limit of 1000 for group member herr
    """
    topic.group = self
    topic.author = user
    
    topic.put()
    
    topic.add_subscribers(self.get_member_keys(limit=1000))
    topic.notify_subscribers()
    
  
  def delete_topic(self, topic):
    """docstring for delete_topic"""
    topic.undo_notify()
    topic.delete()
  
  def latest_topics_by_user(self, user limit=24, offset=0):
    """docstring for get_topics"""
    return self.latest_by_subscriber(user, limit=limit, offset=offset)
  

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
    return self.has_author(user)

  def can_delete(self, user):
    """docstring for can_delete"""
    return self.has_author(user)
  
  def has_author(self, user):
    """docstring for has_author"""
    return self.author.key() == user.key()

  #######
  #
  # post related apis
  #
  #######

  def can_create_post(self, user):
    """docstring for can_create_thread"""
    return self.can_view(user) and user != Guest
  
  def can_delete_post(self, user):
    """docstring for can_delete_post"""
    return False
  
  def create_post(self, post, user):
    """docstring for add_group_post"""
    post.author = user
    post.put()
    
    self.notify_subscribers()

  def delete_post(self, post):
    """docstring for delete_post"""
    post.delete()
  
  def get_posts(self, user, limit=24, offset=0):
    """docstring for get_posts"""
    return GroupPost.all().filter("topic =", self).order("create_at")
  
class GroupPost(ndb.Message):
  """docstring for Post"""
  author = db.ReferenceProperty(User)
  topic = db.ReferenceProperty(Topic)
  content = db.TextFlyProperty()
