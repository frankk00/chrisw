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
  create_date = db.DateProperty(auto_now_add=True)
  password = db.StringProperty(required=True)
  email = db.EmailProperty(required=True)
  