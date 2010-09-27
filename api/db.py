#!/usr/bin/env python
# encoding: utf-8
"""
db.py

A patch for Google appengine's db module

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging
import datetime
import time

from google.appengine.ext import db
from google.appengine.ext.db import *
from google.appengine.api import datastore_errors

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_dict(model):
  output = {}
  
  for key, prop in model.properties().iteritems():
    
    try:
      value = getattr(model, key)
    except datastore_errors.Error:
      value = None
    
    if value is None or isinstance(value, SIMPLE_TYPES):
      output[key] = value
    elif isinstance(value, datetime.date):
      # Convert date/datetime to ms-since-epoch ("new Date()").
      ms = time.mktime(value.utctimetuple()) * 1000
      ms += getattr(value, 'microseconds', 0) / 1000
      output[key] = int(ms)
    elif isinstance(value, db.Model):
      output[key] = to_dict(value)
    else:
      raise ValueError('cannot encode ' + repr(prop))
  
  return output
    
class Model(db.Model):
  """docstring for Model"""
  def to_dict(self):
    return to_dict(self)
  
  def update_model(self, values):
    for k, v in values.iteritems():
      setattr(self, k, v)
  

