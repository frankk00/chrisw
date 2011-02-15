#!/usr/bin/env python
# encoding: utf-8
"""
handlers.py

Created by Kang Zhang on 2011-02-15.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from api.webapp import api_enabled, view_method

from google.appengine.ext import webapp

from chrisw.core import router
from chrisw.core.exceptions import CannotResolvePath

class BaseHandler(webapp.RequestHandler):
  """docstring for BaseHandler"""
  def __init__(self):
    super(BaseHandler, self).__init__()
  
  def get(self, *args):
    """docstring for get"""
    return self.handle_request('get', *args)
  
  def post(self, *args):
    """docstring for post"""
    return self.handle_request('post', *args)
  
  def put(self, *args):
    """docstring for put"""
    return self.handle_request('put', *args)
  
  def head(self, *args):
    """docstring for head"""
    return self.handle_request('head', *args)
  
  def delete(self, *args):
    """docstring for delete"""
    return self.handle_request('delete', *args)
  
  def options(self, *args):
    """docstring for options"""
    return self.handle_request('options', *args)
  
  def trace(self, *args):
    """docstring for trace"""
    return self.handle_request('trace', *args)
    
  def handle_request(self, request_type, *args):
    """docstring for handle_request"""
    path = self.request.path
    handler_func = router.resolve_path(path, request_type)
    
    if handler_func:
      api_enabled(handler_func)(self, *args)
    else:
      #exception happend  
      raise CannotResolvePath(path)
  
def get_handler_bindings():
  """docstring for get_handler_bindings"""
  pathes = router.get_all_pathes()
  return [(path, BaseHandler) for path in pathes]
