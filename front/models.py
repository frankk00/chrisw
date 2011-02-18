#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw import db
from chrisw.i18n import _

class Site(db.Model):
  """a faked object"""
  site_name = db.StringProperty(required=True, default="Daoshicha.com")
  site_slogan = db.StringProperty(required=True, default= _("Want to be the best open source SNS!"))
  @classmethod
  def get_instance(cls):
    """docstring for get_instance"""
    instance = super(Site, cls).all().get()
    if not instance:
      instance = Site()
      instance.put()
      
    return instance

class UHome(db.Model):
  """A faked object for the user management"""
  
  @classmethod
  def get_instance(cls):
    """docstring for get_instance"""
    instance = super(UHome, cls).all().get()
    if not instance:
      instance = UHome()
      instance.put()
      
    return instance
    

class Photo(db.Model):
  """docstring for ProfilePhoto"""
  blob_key = db.StringProperty()
  url = db.StringProperty()
    