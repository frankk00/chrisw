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

class Relation(db.Model):
  """docstring for Relation"""
  relation = db.StringProperty(required=True)
  source = db.StringProperty(required=True)
  target = db.StringProperty(required=True)
  
class Stream(db.FlyModel):
  """docstring for Stream"""
  author = db.StringProperty(required=True)

class Subscription(db.Model):
  """docstring for Subscription"""
  subscribers = db.ReferenceProperty(required=True)

    