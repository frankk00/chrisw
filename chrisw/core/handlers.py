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

class RequestHandlerMeta(type):
  """docstring for RequestHandlerMeta"""
  def __new__(cls, name, bases, attrs):
    """Thanks God, there is something called MetaClass!!!!      
                                                     -- Kang Zhang 2011-02-17      
    """
    
    """"Metaclasses are deeper magic than 99% of users should ever worry
    about. If you wonder whether you need them, you don't (the people who
    actually need them know with certainty that they need them, and don't
    need an explanation about why). -- Python Guru Tim Peters"
    """
    
    """
    Note that decorate the instance method in Python, the only way would be
    using Meta class. The most important reason for this is the im_self field
    in the function object. It seems that field will be initialized after the
    __new__ method from meta class, but before the __init__ method of instance
    class.
    """
    
    """
    If you still can't understand the aboving words, refer to 
      '''http://mail.python.org/pipermail/tutor/2003-December/026707.html'''.
    """
    
    wrap_method_list = ['get', 'post', 'put', 'head', 'delete', 'options', 
      'trace']
    
    for attr, handler_func in attrs.items():
      if attr in wrap_method_list and callable(handler_func):
        attrs[attr] = api_enabled(attrs[attr])
    
    return super(RequestHandlerMeta, cls).__new__(cls, name, bases, attrs)

class RequestHandler(webapp.RequestHandler):
  """docstring for RequestHandler"""
  __metaclass__ = RequestHandlerMeta
        
def get_handler_bindings():
  """docstring for get_handler_bindings"""
  pathes = router.get_all_pathes()
  return [(path, BaseHandler) for path in pathes]
