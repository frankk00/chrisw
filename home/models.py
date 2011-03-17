#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw import db
from chrisw.i18n import _
from chrisw.core.memcache import *

class Site(db.Model):
  """a faked object"""
  site_name = db.StringProperty(required=True, default= _("Daoshicha.com"))
  site_slogan = db.StringProperty(required=True, default= _("Want to be the best open source SNS!"))
  
  @classmethod
  @cache_result('global-site', 240)
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
  @cache_result('uhome-site', 240)
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
    