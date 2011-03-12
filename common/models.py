#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2011-03-09.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw import db

def _get_type_name(cls):
  """docstring for _get_type_name"""
  if isinstance(cls, type):
    return cls.__name__
  return cls.__class__.__name__

class Entity(db.FlyModel):
  """docstring for Entity"""
  create_at = db.DateTimeProperty(auto_now_add=True)
  
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
    relations = self._get_relations(relation, target)
    for rel in relations:
      rel.delete()
  
  def get_target_keys(self, relation, target_type, limit=24):
    """docstring for get_by_relation"""
    return [x.target for x in Relation.all(source=self, relation=relation,\
                        target_type=_get_type_name(target_type)).fetch(limit)]
  
  def get_source_keys(self, relation, source_type, limit=24):
    """docstring for get_source_by_relation"""
    return [x.source for x in Relation.all(relation=relation, target=self,\
                        source_type=_get_type_name(source_type)).fetch(limit)]

class Relation(db.Model):
  """docstring for Relation"""
  relation = db.StringProperty(required=True)
  source = db.WeakReferenceProperty(required=True)
  source_type = db.StringProperty(required=True)
  target = db.WeakReferenceProperty(required=True)
  target_type = db.StringProperty(required=True)
  
  def __init__(self, *args, **kwargs):
    """docstring for __init__"""
    kwargs['source_type'] = kwargs.get('source').__class__.__name__
    kwargs['target_type'] = kwargs.get('target').__class__.__name__
    
    super(Relation, self).__init__(*args, **kwargs)
    
  @classmethod
  def all(cls, **kwargs):
    """docstring for get_sources_by_relation"""
    query = super(Relation, cls).all(**kwargs)
    
    for f in ('source', 'relation', 'target', 'source_type', 'target_type'):
      if kwargs.has_key(f) and kwargs[f] is not None:
        query = query.filter(f, kwargs[f])
    
    return query    

class Subscription(db.Model):
  """docstring for Subscription"""
  subscriber = db.WeakReferenceProperty(required=True)
  subscriber_type = db.StringProperty(required=True)
  topic = db.WeakReferenceProperty(required=True)
  topic_type = db.StringProperty(required=True)
  
  def __init__(self, *args, **kwargs):
    """docstring for __init__"""
    kwargs['subscriber_type'] = kwargs.get('subscriber').__class__.__name__
    kwargs['topic_type'] = kwargs.get('topic').__class__.__name__
    
    super(Relation, self).__init__(*args, **kwargs)
  
  @classmethod
  def all(cls, **kwargs):
    """docstring for all"""
    query = super(Subscription, cls).all(**kwargs)
    
    for f in ('subscriber', 'topic', 'subscriber_type', 'topic_type'):
      if kwargs.has_key(f) and kwargs[f] is not None:
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
                         target_type=self.get_type_name())
    index.put()
  
  def get_type_name(self):
    """docstring for get_type_name"""
    return self.__class__.get_cls_type_name()
  
  @classmethod
  def get_cls_type_name(cls):
    """docstring for get_message_type_name"""
    return cls.__name__
    
  @classmethod
  def latest_by_user(cls, user, limit=24):
    """docstring for all_by_user"""
    indexes = MessageIndex.all(subscribers=user, \
                               target_type=cls.get_cls_type_name())\
                                 .order('-create_at').fetch(limit)
    return db.get([index.target for index in indexes])

class MessageIndex(db.Model):
  """docstring for MessageIndex"""
  subscribers = db.StringListProperty(required=True)
  target = db.WeakReferenceProperty(required=True)
  target_type = db.StringProperty(required=True)
  create_at = db.DateTimeProperty(auto_now_add=True)

