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
  pass

class Relation(db.Model):
  """docstring for Relation"""
  relation = db.StringProperty(required=True)
  source = db.StringProperty(required=True)
  target = db.StringProperty(required=True)
  
class Subscription(db.Model):
  """docstring for Subscription"""
  subscriber = db.StringProperty(required=True)
  topic = db.StringProperty(required=True)

class Message(db.FlyModel):
  """docstring for Message"""
  author = db.ReferenceProperty(required=True)
  create_at = db.DateTimeProperty(required=True)

class MessageIndex(db.Model):
  """docstring for MessageIndex"""
  subscribers = db.StringListProperty(required=True)
  target = db.ReferenceProperty(required=True)
  create_at = db.DateTimeProperty(auto_now_add=True)

    