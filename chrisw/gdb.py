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
  """Return the type name for given class or instance"""
  if isinstance(cls, type):
    return cls.__name__
  return cls.__class__.__name__

class Entity(db.FlyModel):
  """The base model for graph node"""
  create_at = db.DateTimeProperty(auto_now_add=True)
  
  def link(self, link_type, target):
    """Add a link between ``self`` and ``target`` with given ``link_type``
    
    link_type -- a string to specify the type of the link.
    """
    # unlink previous links
    self.unlink(link_type, target)
    
    link = Link(source=self, link_type=link_type, target=target)
    link.put()
    
  def has_link(self, link_type, target):
    """Return if there exist a link between ``self`` and ``target``
    
    link_type -- a string to specify the type of the link.
    """
    return self._get_links(link_type, target).get() is not None
  
  def _get_links(self, link_type, target):
    return Link.all(source=self, link_type=link_type, target=target)
  
  def unlink(self, link_type, target):
    """Remove the given type of link between ``self`` and ``target``"""
    links = self._get_links(link_type, target)
    for link in links:
      link.delete()
  
  def get_targets(self, link_type, target_type, keys_only=False):
    """Return all target entities by given link type and source entity.
    
    keys_only -- if only keys will be loaded.
    """
    query = db.MapQuery(Link.all(source=self, link_type=link_type,\
      target_type=_get_type_name(target_type)), lambda x: x.target)
    
    if not keys_only:
      query = db.GetQuery(query)
    
    return query;
  
  @classmethod
  def get_sources(cls, link_type, target, keys_only=False):
    """Return all source entities by given link type and target entity.
    
    keys_only -- if only keys will be loaded.
    """
    query = db.MapQuery(Link.all(link_type=link_type, target=target,\
      source_type=_get_type_name(cls)), lambda x: x.source)
    
    if not keys_only:
      query = db.GetQuery(query)
    
    return query
  
  @classmethod
  def latest(cls):
    """Return the latest created entities"""
    return cls.all().order("-create_at")

class Link(db.Model):
  """The model for the link between entites"""
  link_type = db.StringProperty(required=True)
  source = db.WeakReferenceProperty(required=True)
  source_type = db.StringProperty(required=True)
  target = db.WeakReferenceProperty(required=True)
  target_type = db.StringProperty(required=True)
  
  def __init__(self, *args, **kwargs):
    for attr in ('source', 'target'):
      if kwargs.has_key(attr):
        kwargs[attr + '_type'] = _get_type_name(kwargs.get(attr))
    
    super(Link, self).__init__(*args, **kwargs)
  
    
class Subscription(db.Model):
  """The relation between entities and messages"""
  subscriber = db.WeakReferenceProperty(required=True)
  subscriber_type = db.StringProperty(required=True)
  topic = db.WeakReferenceProperty(required=True)
  topic_type = db.StringProperty(required=True)
  
  def __init__(self, *args, **kwargs):
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
  """The model which represent the message in system"""
  create_at = db.DateTimeProperty(auto_now_add=True)
  update_at = db.DateTimeProperty(auto_now=True)
  
  def add_subscriber(self, users):
    """Add a or a set of subscriber for message. It's designed for Quora liked
     apps.
    """
    if isinstance(users, db.Model):
      users = [users]
      
    for user in users:
      s = Subscription(subscriber=user, topic=self, \
                       topic_type=self.get_type_name())
      s.put()
  
  def add_subscribers(self, users):
    """Deprecated method"""
    self.add_subscriber(users)
  
  def _get_subscriptions(self, user):
    return Subscription.all(subscriber=user, topic=self)
  
  def delete_subscriber(self, user):
    """Remove a subscriber from message"""
    db.delete(self._get_subscriptions(user))
  
  def has_subscriber(self, user):
    """Return if this message has the given user as subscriber"""
    return self._get_subscriptions(user).get() != None
  
  def get_subscribers(self, keys_only=False):
    """Return all subscribers of this message.
    
    keys_only -- if only keys will be loaded.
    """
    query = db.MapQuery(self._get_subscriptions(None), lambda x:x.subscriber)
    
    if not keys_only:
      query = db.GetQuery(query)
    
    return query;
  
  def notify(self, users=None):
    """Notify the given users for this message's update"""
    if not users:
      users = self.get_subscribers(keys_only=True)
    self._notify_users(users)
  
  def redo_notify(self):
    """Redo the notification"""
    index = MessageIndex.all(target=self).get()
    
    if index:
      index.put()
  
  def _notify_users(self, users):
    """Internal methods for notification"""
    keys = _init_user_keys(users)
    
    index = MessageIndex.all(target=self).get()
    
    if not index:
      index = MessageIndex(subscribers=keys, target=self,\
                         target_type=self.get_type_name())
    
    index.subscribers = keys
    
    index.put()
  
  def undo_notify(self):
    """Cancel all notification for this message"""
    db.delete(MessageIndex.all(target=self, keys_only=True))
  
  def get_type_name(self):
    """Return the entity type name for instance"""
    return self.__class__.get_cls_type_name()
  
  @classmethod
  def get_cls_type_name(cls):
    """Return the entity type name for class"""
    return cls.__name__
  
  @classmethod
  def latest_by_subscriber(cls, user, keys_only=False):
    """Get all latest messages for given subscriber"""
    query = db.MapQuery(MessageIndex.all(subscribers=user, \
      target_type=cls.get_cls_type_name()).order('-update_at'),
      lambda x: x.target)
    
    if not keys_only:
      query = db.GetQuery(query)
    
    return query
  
  @classmethod
  def latest(cls):
    """Return latest created messages"""
    return cls.all().order("-create_at")

class MessageIndex(db.Model):
  """docstring for MessageIndex"""
  subscribers = db.StringListProperty(required=True)
  target = db.WeakReferenceProperty(required=True)
  target_type = db.StringProperty(required=True)
  create_at = db.DateTimeProperty(auto_now_add=True)
  update_at = db.DateTimeProperty(auto_now=True)
  
  @classmethod
  def all(cls, **kwargs):
    if kwargs.has_key('subscribers'):
      value = kwargs['subscribers']
      if isinstance(value, db.Model):
        value = value.key()
      if not isinstance(value, db.Key):
        raise Exception('Subscriber must be key or model %s' % value)
      value = str(value)
      kwargs['subscribers'] = value
    
    return super(MessageIndex, cls).all(**kwargs)
