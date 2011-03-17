#!/usr/bin/env python
# encoding: utf-8
"""
gdb.py

Graph Database module for SNS liked application. It could be used to describe 
the *Network* between humans, and be used to broadcast the updates info of 
specified entities.

Created by Kang Zhang on 2011-03-09.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw.db import *
from chrisw import db

def _get_type_name(cls):
  """docstring for _get_type_name"""
  if isinstance(cls, type):
    return cls.__name__
  return cls.__class__.__name__

class Entity(db.FlyModel):
  """docstring for Entity"""
  create_at = db.DateTimeProperty(auto_now_add=True)
  
  def link(self, link_type, target):
    """docstring for create_link_with"""
    # unlink previous links
    self.unlink(link_type, target)
    
    link = Link(source=self, link_type=link_type, target=target)
    link.put()
    
  def has_link(self, link_type, target):
    """docstring for has_link_with"""
    return self._get_links(link_type, target).get() is not None
  
  def _get_links(self, link_type, target):
    """docstring for get_links"""
    return Link.all(source=self, link_type=link_type, target=target)
  
  def unlink(self, link_type, target):
    """docstring for remove_link_with"""
    links = self._get_links(link_type, target)
    for link in links:
      link.delete()
  
  def get_target_keys(self, link_type, target_type):
    """docstring for get_by_link"""
    return db.MapQuery(Link.all(source=self, link_type=link_type,\
      target_type=_get_type_name(target_type)), lambda x: x.target)
  
  @classmethod
  def get_source_keys(cls, link_type, target):
    """docstring for get_source_by_link"""
    return db.MapQuery(Link.all(link_type=link_type, target=target,\
      source_type=_get_type_name(cls)), lambda x: x.source)

class Link(db.Model):
  """docstring for Link"""
  link_type = db.StringProperty(required=True)
  source = db.WeakReferenceProperty(required=True)
  source_type = db.StringProperty(required=True)
  target = db.WeakReferenceProperty(required=True)
  target_type = db.StringProperty(required=True)
  
  def __init__(self, *args, **kwargs):
    """docstring for __init__"""
    for attr in ('source', 'target'):
      if kwargs.has_key(attr):
        kwargs[attr + '_type'] = _get_type_name(kwargs.get(attr))
    
    super(Link, self).__init__(*args, **kwargs)
  
    
class Subscription(db.Model):
  """docstring for Subscription"""
  subscriber = db.WeakReferenceProperty(required=True)
  subscriber_type = db.StringProperty(required=True)
  topic = db.WeakReferenceProperty(required=True)
  topic_type = db.StringProperty(required=True)
  
  def __init__(self, *args, **kwargs):
    """docstring for __init__"""
    for attr in ('subscriber',):
      if kwargs.has_key(attr):
        kwargs[attr + '_type'] = _get_type_name(kwargs.get(attr))
    
    super(Subscription, self).__init__(*args, **kwargs)
    
def _init_user_keys(users):
  """docstring for _init_users"""
  
  keys = []
  for user in users:
    if isinstance(user, db.Key):
      key = user
    elif isinstance(user, db.Model):
      key = user.key()
    else:
      raise Exception("User must be Model or Key, %s detected " % user)
    keys.append(str(key))
  return list(set(keys))
  
class Message(db.FlyModel):
  """docstring for Message"""
  create_at = db.DateTimeProperty(auto_now_add=True)
  update_at = db.DateTimeProperty(auto_now=True)
  
  def add_subscriber(self, users):
    """docstring for subscribe"""
    if isinstance(users, db.Model):
      users = [users]
      
    for user in users:
      s = Subscription(subscriber=user, topic=self, \
                       topic_type=self.get_type_name())
      s.put()
  
  def add_subscribers(self, users):
    """docstring for add_subscriber"""
    self.add_subscriber(users)
  
  def _get_subscriptions(self, user):
    """docstring for _get_subscriptions"""
    return Subscription.all(subscriber=user, topic=self)
  
  def delete_subscriber(self, user):
    """docstring for delte_subscriber"""
    db.delete(self._get_subscriptions(user))
  
  def has_subscriber(self, user):
    """docstring for has_subcriber"""
    return self._get_subscriptions(user).get() != None
  
  def get_subscriber_keys(self):
    """docstring for get_subscriber_keys"""
    return db.MapQuery(self._get_subscriptions(None), lambda x:x.subscriber)
  
  def notify_subscribers(self):
    """docstring for notify_subscribers"""
    self.notify_users(self.get_subscriber_keys())
  
  def notify_users(self, users):
    """docstring for notify_users"""
    keys = _init_user_keys(users)
    
    index = MessageIndex.all(target=self).get()
    
    if not index:
      index = MessageIndex(subscribers=keys, target=self,\
                         target_type=self.get_type_name())
    
    index.subscribers = keys
    
    index.put()
  
  def undo_notify(self):
    """docstring for undo_notify"""
    db.delete(MessageIndex.all(target=self, keys_only=True))
  
  def get_type_name(self):
    """docstring for get_type_name"""
    return self.__class__.get_cls_type_name()
  
  @classmethod
  def get_cls_type_name(cls):
    """docstring for get_message_type_name"""
    return cls.__name__
  
  @classmethod
  def latest_keys_by_subscriber(cls, user):
    """docstring for all_by_user"""
    return db.MapQuery(MessageIndex.all(subscribers=user, \
      target_type=cls.get_cls_type_name()).order('-update_at'),
      lambda x: x.target)
  
  @classmethod
  def latest_by_subscriber(self, user):
    """docstring for latest_keys_by_subscriber"""
    return db.MapQuery(self.latest_keys_by_subscriber(user), 
      lambda x: db.get(x), True)
  
  @classmethod
  def latest(cls):
    """docstring for latest"""
    return cls.all().order("-update_at")

class MessageIndex(db.Model):
  """docstring for MessageIndex"""
  subscribers = db.StringListProperty(required=True)
  target = db.WeakReferenceProperty(required=True)
  target_type = db.StringProperty(required=True)
  create_at = db.DateTimeProperty(auto_now_add=True)
  update_at = db.DateTimeProperty(auto_now=True)
  
  @classmethod
  def all(cls, **kwargs):
    """docstring for all"""
    if kwargs.has_key('subscribers'):
      value = kwargs['subscribers']
      if isinstance(value, db.Model):
        value = value.key()
      if not isinstance(value, db.Key):
        raise Exception('Subscriber must be key or model %s' % value)
      value = str(value)
      kwargs['subscribers'] = value
    
    return super(MessageIndex, cls).all(**kwargs)
