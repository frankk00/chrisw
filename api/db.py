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
from google.appengine.ext.db import djangoforms
from django import forms


SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_dict(model):
  output = {}
  
  if hasattr(model, 'properties'):
    items = model.properties().iteritems()
  elif hasattr(model, 'items'):
    items = model.items()
    
  if hasattr(model, 'can_visit_key'):
    check_key = model.can_visit_key
  else:
    check_key = None
  
  from duser import auth
  user = auth.get_current_user()
  
  for key, prop in items:
    
    if check_key and not check_key(user, key):
      # can't be visited since privacy control
      continue
      
    try:
      value = getattr(model, key)
    except datastore_errors.Error:
      value = None
    except AttributeError:
      value = prop
    
    if value is None or isinstance(value, SIMPLE_TYPES):
      output[key] = value
    elif isinstance(value, datetime.date):
      # Convert date/datetime to ms-since-epoch ("new Date()").
      logging.debug(" datetime: %s", value)
      ms = time.mktime(value.utctimetuple()) * 1000
      ms += getattr(value, 'microseconds', 0) / 1000
      output[key] = int(ms)
    elif isinstance(value, db.Model):
      output[key] = to_dict(value)
    elif isinstance(value, djangoforms.ModelForm) or \
         isinstance(value, forms.Form):
      output[key] = {'data': to_dict(value.data),
                     'errors': to_dict(value.errors)}
    else:
      logging.debug('Error from api.db: cannot encode ' + repr(prop))
      continue
  
  return output
    
class Model(db.Model):
  """docstring for Model"""
  deleted = db.BooleanProperty(default=False)
  
  def to_dict(self):
    return to_dict(self)
  
  def delete(self, **kwargs):
    """docstring for def delete(self, **kwargs):"""
    self.delete = True
    self.put()
  
  @classmethod
  def get(cls, keys, **kwargs):
    """Notice that this method overrides get_by_id and get_by_key_name
    """
    results = super(Model, cls).get(keys)

    if results is None:
      return None

    if isinstance(results, Model):
      instances = [results]
    else:
      instances = results
    
    # filter the deleted result
    instances = [ i for i in instances if not i.deleted]
    
    if len(instances) == 0:
      return None
    elif len(instances) == 1:
      return instances[0]
    return instances
  
  @classmethod
  def all(cls, **kwargs):
    """Deleted items has been filtered.
    """
    return super(Model, cls).all(**kwargs).filter('deleted = ', False)
  
  @classmethod
  def gql(cls, query_string, *args, **kwds):
    """
    """
    raise Exception("GQL is not allowed in this extension")
  

def main():
  """Testing """
  import json
  from datetime import datetime
  print json.dumps({1:datetime.now()})
  pass
  
  
if __name__ == '__main__':
  main()
