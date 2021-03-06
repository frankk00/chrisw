#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-25.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

from chrisw import db, gdb
from chrisw.core.memcache import cache_result

from common.auth import get_current_user, User, Guest
from conf import settings


GROUP_MEMEBER = 'has-group-member'
GROUP_ADMIN = 'has-group-admin'
RECENT_MEMBER_LIMIT = 20

class GroupSite(db.Model):
  """a faked object"""
  avaliable_group_slots = db.IntegerProperty(required=True, default=100)
  
  def get_all_joined_group_keys(self, user):
    """docstring for get_all_joined_group_keys"""
    return Group.all(creator=user, keys_only=True)
    
  def get_joined_groups(self, user, limit=24, offset=0):
    """docstring for get_groups"""
    return Group.all(creator=user).fetch(limit=limit, offset=offset)
  
  def add_group(self, group, user):
    """add a new group to this site"""
    # Race condition could happen here, but... ... I don't care 
    # Since it just allow users to create more groups than we expect :-)
    self.avaliable_group_slots -= 1
    self.put()
    
    group.creator = user
    group.put()
    
    group.join(user)
    group.add_admin(user)
    
    UserGroupInfo.get_by_user(user).update_group_count()
  
  def delete_group(self):
    """TODO:
    """
    pass
  
  def can_create_group(self, user):
    return self.avaliable_group_slots > 0
  
  @classmethod
  @cache_result('group-site', 240)
  def get_instance(cls):
    """docstring for get_instance"""
    instance = super(GroupSite, cls).all().get()
    if not instance:
      instance = GroupSite()
      instance.put()
      
    return instance

class UserGroupInfo(gdb.Entity):
  """docstring for UserGroupProfile"""
  user = db.ReferenceProperty(required=True)
  
  topic_count = db.IntegerFlyProperty(default=0)
  post_count = db.IntegerFlyProperty(default=0)
  group_count = db.IntegerFlyProperty(default=0)
  
  recent_joined_groups = db.ListFlyProperty(default=[])
  
  def update_topic_count(self):
    """docstring for update_topic_count"""
    self.topic_count = GroupTopic.all(author=self.user).count()
    self.put()
  
  def update_post_count(self):
    """docstring for update_post_count"""
    self.post_count = GroupPost.all(author=self.user).count()
    self.put()
  
  def update_group_count(self):
    """docstring for update_group_count"""
    self.group_count = Group.all(creator=self.user).count()
    self.put()
  
  def get_recent_joined_groups(self):
    """docstring for joined_groups"""
    return db.get(self.recent_joined_groups)
  
  def update_recent_joined_groups(self):
    """docstring for get_joined_groups"""
    self.recent_joined_groups = Group.get_group_keys_by_user(self.user)\
      .fetch(limit=8, offset=0)
    
    logging.debug("recent_joined_groups : %s", self.recent_joined_groups)
    
    self.put()
  
  @classmethod
  def get_by_user(cls, user):
    """docstring for get_by_user"""
    # init all needed object here
    groupinfo = UserGroupInfo.all().filter("user =", user).get()
    if not groupinfo:
      groupinfo = UserGroupInfo(user=user)
      groupinfo.put()
    return groupinfo

class Group(gdb.Entity):
  """docstring for Board"""
  creator = db.ReferenceProperty(User)
  title = db.StringProperty(default='')
  
  introduction = db.TextProperty(default='')
  photo_url = db.StringProperty(default=settings.DEFAULT_GROUP_PHOTO)
  
  recent_members = db.ListFlyProperty(default=[])
  member_count = db.IntegerFlyProperty(default=1)
    
  def can_view(self, user):
    """docstring for can_see"""
    return True
      
  def can_delete(self, user):
    """docstring for can_delete"""
    return self.is_creator(user)
  
  def is_creator(self, user):
    """docstring for is_creator"""
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
    return self.has_member(user) and not self.is_creator(user)
  
  def join(self, user):
    self.link(GROUP_MEMEBER, user)
    
    self._update_member_info()
    
    UserGroupInfo.get_by_user(user).update_recent_joined_groups()
    
  def quit(self, user):
    """docstring for quit"""
    self.unlink(GROUP_MEMEBER, user)
    
    self._update_member_info()
    
    UserGroupInfo.get_by_user(user).update_recent_joined_groups()
    
  def has_member(self, user):
    """docstring for has_member"""
    return self.has_link(GROUP_MEMEBER, user)
  
  def get_latest_joined_members(self):
    """docstring for get_latest_joined_members"""
    return db.get(self.recent_members.reverse())
  
  def get_member_keys(self):
    """docstring for get_members"""
    return self.get_targets(GROUP_MEMEBER, User, keys_only=True)
  
  def get_members(self):
    """docstring for get_members"""
    return db.MapQuery(self.get_member_keys(), lambda x:db.get(x), True)
  
  def _update_member_info(self):
    """docstring for _update_member_count"""
    self.member_count = self.get_member_keys().count()
    self.recent_members = list(self.get_member_keys().fetch(limit=6))
    self.put()
  
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
    return self.is_creator(user)
  
  def can_remove_admin(self, user):
    """docstring for can_remove_admin"""
    return self.is_creator(user)
  
  def add_admin(self, new_admin):
    """docstring for add_admin"""
    return self.link(GROUP_ADMIN, new_admin)
  
  def remove_admin(self, new_admin):
    """docstring for remove_admin"""
    return self.unlink(GROUP_ADMIN, new_admin)
  
  def has_admin(self, user):
    """docstring for has_admin"""
    return self.has_link(GROUP_ADMIN, user)
  
  def _get_admin_keys(self, limit=24, offset=0):
    """deprecated function"""
    return self.get_targets(GROUP_ADMIN, User, limit=limit,\
      offset=offset, keys_only=True)
  
  def _get_admins(self, limit=24, offset=0):
    """deprecated function"""
    return db.get(self.get_admin_keys(self, limit=limit, offset=offset))

  #######
  #
  # topic related apis
  #
  #######

  def can_create_topic(self, user):
    """docstring for can_create_thread"""
    return self.has_member(user) 
  
  def create_topic(self, topic, user):
    """ Create a new topi in group
    TODO: remove the limit of 1000 for group member herr
    """
    topic.group = self
    topic.author = user
    
    topic.put()
    
    subscribers = list(self.get_member_keys()) + [Guest]
    topic.notify(subscribers)
    
    UserGroupInfo.get_by_user(user).update_topic_count()
  
  def delete_topic(self, topic):
    """docstring for delete_topic"""
    topic.undo_notify()
    topic.delete()
  
  def get_all_topics(self, has_order=False):
    """docstring for get_all_topics"""
    query = GroupTopic.all(group=self)
    if has_order: query = query.order('-update_at')
    return query
  
  @classmethod
  def get_group_keys_by_user(cls, user):
    """docstring for get_groups_by_user"""
    return cls.get_sources(GROUP_MEMEBER, user, keys_only=True)

class GroupTopic(gdb.Message):
  """docstring for Thread"""
  author = db.ReferenceProperty(User)
  group = db.ReferenceProperty(Group)
  
  title = db.TextFlyProperty(default='')
  content = db.TextFlyProperty(default='')
  length = db.IntegerFlyProperty(default=0)
  hits = db.IntegerFlyProperty(default=0)
  
  def can_view(self, user):
    """docstring for can_view"""
    return self.group.can_view(user)
  
  def can_edit(self, user):
    """docstring for can_edit"""
    return self.is_author(user)

  def can_delete(self, user):
    """docstring for can_delete"""
    return self.is_author(user)
  
  def is_author(self, user):
    """docstring for is_author"""
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
    post.topic = self
    post.put()
    
    self.length = self.get_all_posts().count()
    self.put()
    
    self.redo_notify()
    
    UserGroupInfo.get_by_user(user).update_post_count()

  def delete_post(self, post):
    """docstring for delete_post"""
    post.delete()
  
  def get_all_posts(self, has_order=False):
    """docstring for get_all_posts"""
    query = GroupPost.all(topic=self)
    if has_order:
      query = query.order("create_at")
    return query
  
  
class GroupPost(gdb.Message):
  """docstring for Post"""
  author = db.ReferenceProperty(User)
  topic = db.ReferenceProperty(GroupTopic)
  content = db.TextFlyProperty(default='')
