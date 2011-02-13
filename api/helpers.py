#!/usr/bin/env python
# encoding: utf-8
"""
helpers.py

Created by Kang Zhang on 2010-10-01.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging
    
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
  logging.debug(" %s ", str(model_obj))
  for name, member in inspect.getmembers(model_obj):
    # logging.debug(" Member %s : %s ", str(name), str(member))
    if inspect.ismethod(member) and name[:4] == 'can_':
      # keep compitable with python 2.5
      args, varargs, keywords, defaults = inspect.getargspec(member)
      if args == ['self', 'user']:
        out[name] = member(user)
  
  return out

class Page(object):
  """docstring for Paginator"""
  def __init__(self, request, offset, limit, count):
    super(Page, self).__init__()
    self.count = count
    self.offset = offset
    self.limit = limit
    self.request = request
    self.page_size = limit - offset
    self.path = request.path
  
  def has_next(self):
    """docstring for has_next"""
    return self.limit < self.count
  
  def has_prev(self):
    """docstring for has_previous"""
    return self.offset != 0
  
  def prev_page(self):
    """docstring for prev_page"""
    return Page(self.request, self.offset - self.page_size, \
      self.limit - self.page_size, self.count)
  
  def next_page(self):
    """docstring for next_page"""
    return Page(self.request, self.offset + self.page_size, \
      self.limit + self.page_size, self.count)
  
  def next_url(self):
    """docstring for next_url"""
    
    logging.debug("URL: " + self.url())
    return self.next_page().url() 
  
  def prev_url(self):
    """docstring for prev_url"""
    return self.prev_page().url()
  
  def url(self):
    """docstring for url"""
    # logging.debug("URL: " + self.path + "?offset=" + self.offset + "&limit=" + self.limit)
    return self.path + "?offset=" + str(self.offset) + "&limit=" + \
      str(self.limit)

# importing helper
# import form fields
from django import forms
try:
  # for django 1.1
  from django.forms import CharField
  from django import forms as fields
except ImportError:
  # django 0.9
  from django.db import models as fields
