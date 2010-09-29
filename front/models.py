#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from api import db

class UHome(db.Model):
  """A faked object for the user management"""
  pass
    

class Photo(db.Model):
  """docstring for ProfilePhoto"""
  blob_key = db.StringProperty()
  url = db.StringProperty()
    