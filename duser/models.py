#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from google.appengine.ext import db
from google.appengine.api import users


class User(db.Model):
  """docstring for User"""
  uid = db.StringProperty(required=True)
  username = db.StringProperty(required=True)
  create_date = db.DateTimeProperty(auto_now_add=True)
  password = db.StringProperty(required=True)
  email = db.EmailProperty(required=True)
  
  def can_visit_key(self, user, key):
    """docstring for visible"""
    if key == 'password':
      return False
    elif key == 'email':
      # can be visible by the user himself
      return user and user.uid == self.uid
    return True
  