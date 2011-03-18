#!/usr/bin/env python
# encoding: utf-8
"""
memcache.py

Created by Kang Zhang on 2011-03-13.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from google.appengine.api import memcache
from google.appengine.api.memcache import *

from chrisw import db

from conf import settings

def _format_key(keyformat, *args, **kwargs):
  """docstring for _format_key"""
  
  if args and kwargs:
    raise Exception("Cannot format memcache using both *args and **kwargs")
  
  key = keyformat
  
  if args:
    args = map(lambda x: x.key() if isinstance(x, db.Model) else x, args)
    key = keyformat % args[0:keyformat.count('%')]
  else:
    key = keyformat % kwargs
  
  return key

def cache_result(keyformat, time=60):
  """Decorator to memoize functions using memcache."""
  def decorator(fxn):
    def wrapper(*args, **kwargs):
      
      key = _format_key(keyformat, *args, **kwargs)
      data = memcache.get(key)
      if data is not None:
        return data
      data = fxn(*args, **kwargs)
      memcache.set(key, data, time)
      
      return data
    return wrapper
    
  return decorator if settings.ENABLE_CACHE else lambda x:x



def cache_action(keyformat, time=60):
  """docstring for cache_action"""
  def decorator(func):
    def wrapper(*args, **kwargs):
      """docstring for wrapper"""
      from chrisw.core.action import cache
      
      key = _format_key(keyformat, *args, **kwargs)

      return cache(func, args, kwargs, key, time)
    return wrapper
    
  return decorator if settings.ENABLE_CACHE else lambda x:x