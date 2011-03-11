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

class Relation(db.Model):
  """docstring for Relation"""
  relation = db.StringProperty(required=True)
  source = db.WeakReferenceProperty(required=True)
  target = db.WeakReferenceProperty(required=True)
  
  @classmethod
  def get_by_relation(cls, relation):
    """docstring for get_sources_by_relation"""
    cls.all().filter('relation =', relation)
  
  @classmethod
  def get_by_source(cls, source):
    """docstring for get_by_source"""
    cls.all().filter('source =', source)
  
  @classmethod
  def get_by_target(cls, target):
    """docstring for get_by_target"""
    cls.all().filter('target =', target)
  
  @classmethod
  def get_by_relation_and_target(cls, relation, target):
    """docstring for get_source_by_relation"""
    cls.get_by_relation(relation).filter('target =', target)
  
  @classmethod
  def get_by_source_and_relation(cls, source, relation):
    """docstring for get_by_source_and_relation"""
    cls.get_by_relation(relation).filter('source =', source)
  
class Subscription(db.Model):
  """docstring for Subscription"""
  subscriber = db.WeakReferenceProperty(required=True)
  topic = db.WeakReferenceProperty(required=True)
  
  @classmethod
  def get_by_topic(cls, topic):
    """docstring for get_by_topic"""
    cls.all().filter('topic =', topic)
  
  @classmethod
  def get_by_subscriber(cls, subscriber):
    """docstring for get_by_subscriber"""
    cls.all().filter('subscriber =', subscriber)

class Message(db.FlyModel):
  """docstring for Message"""
  author = db.ReferenceProperty(required=True)
  create_at = db.DateTimeProperty(required=True)

class MessageIndex(db.Model):
  """docstring for MessageIndex"""
  subscribers = db.ListProperty(db.Key, required=True)
  target = db.ReferenceProperty(required=True)
  create_at = db.DateTimeProperty(auto_now_add=True)
