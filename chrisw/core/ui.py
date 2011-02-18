#!/usr/bin/env python
# encoding: utf-8
"""
ui.py

Created by Kang Zhang on 2011-02-18.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from api.webapp import PermissionUI, view_method

def not_view_method(func):
  """docstring for not_view_method"""
  func.im_not_view_method = True
  return func

class ModelUIMeta(type):
  """docstring for ModelUIMeta"""
  def __new__(cls, name, bases, attrs):
    """docstring for __new__"""
    
    for attr, item in attrs.items():
      if attr[0] is not '_' and callable(item) and \
        not hasattr(item, 'im_not_view_method'):
          attrs[attr] = view_method(item)
    
    return super(ModelUIMeta, cls).__new__(cls, name, bases, attrs)
    

class ModelUI(PermissionUI):
  """docstring for ModelUI"""
  
  __metaclass__ = ModelUIMeta
  
