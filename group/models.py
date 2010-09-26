#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-25.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from google.appengine.ext import db
from google.appengine.api import users

from duser import User

class Group(db.Model):
  """docstring for Board"""
  create_time = db.DateTimeProperty(auto_now_add=True)
  title = db.StringProperty()
  introduction = db.TextProperty()
  create_user = db.ReferenceProperty(User)
  admin_users = db.StringListProperty()

class Topic(db.Model):
  """docstring for Thread"""
  create_time = db.DateTimeProperty(auto_now_add=True)
  update_time = db.DateTimeProperty(auto_now_add=True)
  create_user = db.ReferenceProperty(User)
  title = db.TextProperty()
  content = db.TextProperty()
  group = db.ReferenceProperty(Group)
  
class Post(db.Model):
  """docstring for Post"""
  create_time = db.DateTimeProperty(auto_now_add=True) 
  create_user = db.ReferenceProperty(User)
  topic = db.ReferenceProperty(Topic)
  content = db.TextProperty()

