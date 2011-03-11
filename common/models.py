#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2011-03-09.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw import db

class Entity(db.FlyModel):
  """docstring for Entity"""
  create_at = db.DateTimeProperty(required=True)
  
  def create_relation(self, relation, target):
    """docstring for create_relation_with"""
    rel = Relation(source=self, relation=relation, target=target)
    rel.put()
    
  def has_relation(self, relation, target):
    """docstring for has_relation_with"""
    return self._get_relations(relation, target).get() is not None
  
  def _get_relations(self, relation, target):
    """docstring for get_relations"""
    return Relation.all(source=self, relation=relation, target=target)
  
  def delete_relation(self, relation, target):
    """docstring for remove_relation_with"""
    relations = self._get_relations(relation, target).fetch()
    for rel in relations:
      rel.delete()
  
  
  def get_target(self, relation, limit=24):
    """docstring for get_by_relation"""
    return [x.target for x in Relation.all(source=self, relation=relation)\
                                      .fetch(limit)]
  
  def get_source(self, relation, limit=24):
    """docstring for get_source_by_relation"""
    return [x.source for x in Relation.all(relation=relation, target=self)\
                                      .fetch(limit)]

class Relation(db.Model):
  """docstring for Relation"""
  relation = db.StringProperty(required=True)
  source = db.WeakReferenceProperty(required=True)
  target = db.WeakReferenceProperty(required=True)
  
  @classmethod
  def all(cls, **kwargs):
    """docstring for get_sources_by_relation"""
    query = super(Relation, cls).all(**kwargs)
    
    for f in ('source', 'relation', 'target'):
      if kwargs.has_key(f):
        query = query.filter(f, kwargs[f])
    
    return query
    
class Subscription(db.Model):
  """docstring for Subscription"""
  subscriber = db.WeakReferenceProperty(required=True)
  topic = db.WeakReferenceProperty(required=True)
  
  @classmethod
  def all(cls, **kwargs):
    """docstring for all"""
    query = super(Subscription, cls).all(**kwargs)
    
    for f in ('subscriber', 'topic'):
      if kwargs.has_key(f):
        query = query.filter(f, kwargs[f])
    
    return query
  
def _init_user_keys(users):
  """docstring for _init_users"""
  from duser.models import Guest
  # also putinto guest inbox
  users.append(Guest)
  
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
  author = db.ReferenceProperty(required=True)
  create_at = db.DateTimeProperty(auto_now_add=True)
  
  def add_subscriber(self, user):
    """docstring for subscribe"""
    s = Subscription(subscriber=user, topic=self)
    s.put()
  
  def _get_subscriptions(self, user):
    """docstring for _get_subscriptions"""
    return Subscription.all(subscriber=user, topic=self)
  
  def delte_subscriber(self, user):
    """docstring for delte_subscriber"""
    for s in self._get_subscriptions().fetch():
      s.delete()
  
  def has_subcriber(self, user):
    """docstring for has_subcriber"""
    return self._get_subscriptions().get() != None
  
  def get_subscriber_keys(self):
    """docstring for get_subscriber_keys"""
    return [s.subscriber for s in self._get_subscriptions().fetch()]
  
  def notify_subscribers(self):
    """docstring for notify_subscribers"""
    self.notify_users(self.get_subscriber_keys())
  
  def notify_users(self, users):
    """docstring for notify_users"""
    keys = _init_user_keys(users)
    
    index = MessageIndex(subscribers=keys, target=self,\
                         type_name=self.type_name)
    index.put()
    
  @classmethod
  def latest_by_user(self, user, limit=24):
    """docstring for all_by_user"""
    keys = MessageIndex.all(subscribers=user, target=self).order('-create_at')\
                       .fetch(limit)
    return db.get(keys)
  
  type_name = 'basic_message'

class MessageIndex(db.Model):
  """docstring for MessageIndex"""
  subscribers = db.StringListProperty(required=True)
  target = db.WeakReferenceProperty(required=True)
  type_name = db.StringProperty(required=True)
  create_at = db.DateTimeProperty(auto_now_add=True)

