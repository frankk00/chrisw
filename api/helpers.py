#!/usr/bin/env python
# encoding: utf-8
"""
helpers.py

Created by Kang Zhang on 2010-10-01.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from duser.auth import Guest

def inspect_permissions(model_obj, user = Guest):
  """Inspect the model object to get possible permissions
  
  The model's permission method neeeds start with "can_", while it contains
  and only contains two arguments ['self', 'user']:
  Example:
  
  class StoreModel(db.Model):
    def can_edit(self, user):
      return True
  
  """
  out = {}
  
  import inspect
  for member in inspect.getmembers(model_obj):
    if inspect.isfunction(member):
      func_name = member.__name__
      if func_name[:4] == 'can_':
        args = inspect.getargspec(member).args
        if args == ['self', 'user']:
          out[func_name] = member(model_obj, user)
  
  return out