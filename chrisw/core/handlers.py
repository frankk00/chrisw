#!/usr/bin/env python
# encoding: utf-8
"""
handlers.py

Created by Kang Zhang on 2011-02-15.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

from common.auth import get_current_user, Guest

from google.appengine.ext import webapp

from chrisw.core import router, exceptions
from chrisw.core.exceptions import CannotResolvePath

from action import *

try:
  import json
except Exception, e:
  # before appengine's python upgrade to 2.7, we need import json from django
  from django.utils import simplejson as json


class APIError(exceptions.ChriswException):
  """docstring for APIError"""
  def __init__(self, reason):
    super(APIError, self).__init__(reason)
    self.reason = reason

class UnknownActionException(exceptions.ChriswException):
  """docstring for UnknownActionException"""
  def __init__(self, action):
    super(UnknownActionException, self).__init__(str(action))
    self.reason = "Can't recognized Action: " + str(action)
    

def login_required(func):
  """
  Usage:
  @login_required
  def post(self):
    pass
  """
  from common.auth import get_current_user

  def wrapper(self, *args, **kwargs):
    """docstring for wrapper"""

    if get_current_user() != Guest:
      return func(self, *args, **kwargs)
    else:
      import home
      return self.redirect(home.create_login_url(self.request.url))

  return wrapper

def filter_result(result, fields_dict):
  """docstring for filter_result"""
  output = result
  if fields_dict:
    output = {}
    keys = fields_dict['fields']
    for key in keys:
      result_key = key
      
      if key[0] == '$': # trim the starting $
        result_key = key[1:]
      
      output[key] = filter_result(result[key], fields_dict.get(key, {}))
  return output

def api_enabled(func):
  """
  To enable a handler's result can be returned as JSON object.
  
  For a handler on 
    /example/path/to/handler
  The JSON result can be accesssed from
    /example/path/to/handler?result_type=json
  
  Useage:
  @api_enabled
  def get(self):
    return template('template-name.html', varible_dict)
  
  The return type of the handler can be
    1. template_name, var_dict . will be rendered with var_dict using template
      named template_name.
    2. new_url. will be directed to the new url.
    3. a exception raised from the method. will be wrapped with error:{}
  
  """
  
  def wrapper(self, *args, **kwargs):
    """docstring for wrapper"""
    result_type = self.request.get('result_type', default_value="html")  
    fields = self.request.get('fields', default_value="{}")
    error = None
    fields_dict = {}
    
    try:
      action = func(self, *args, **kwargs)
      fields_dict = json.loads(fields)
      
    except exceptions.ChriswException, e:
      # api execute fault
      error = 'API Execution error' + e.msg
    except ValueError, e:
      # fields parse fault
      error, fields_dict = 'API fields error: ' + str(e), {}
    finally:
      if error:
        action = template('error.html', {'error':error})
        action.status = 'error'
    
    if isinstance(action, back):
      from_url = self.request.headers.get('Referer','/')
      if from_url == self.request.url:
        action = template('error.html', {'error':"Visiting loop"})
      else:
        action = redirect(from_url)
    elif isinstance(action, login):
      from home import create_login_url
      action = redirect(create_login_url(self.request.url))
    elif isinstance(action, template):
      # for debugging
      # var_dict.update({'site_message':"You've created a new group."})
      pass
    elif isinstance(action, redirect) or isinstance(action, cache):
      pass
    else:
      raise UnknownActionException(action)
    
    if result_type == 'html':
      
      if isinstance(action, redirect):
        # redirect action
        return self.redirect(action.to_url)
      
      # template action
      result_string = action.render_to_string()
    elif result_type == 'json':
      
      if isinstance(action, template):
        action_name = 'render' # means template
        data_dict = action.var_dict
      else:
        action_name = 'redirect'
        # here is the trick :-)
        data_dict = {"to_url": action.to_url}
      
      from chrisw.db import to_dict
      result_dict = filter_result(to_dict(data_dict),fields_dict)
      
      response_dict = {'status': action.status,
                       'action': {
                          'cmd': action_name,
                          'data': result_dict
                          },
                       'error': error,
                       }
      
      result_string = json.dumps(response_dict, sort_keys=False, indent=4)
    
    return self.response.out.write(result_string)
    
    
  return wrapper

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
    handler = router.resolve_path(path, request_type)
    
    if handler:
      import inspect
      
      if inspect.isclass(handler):
        handler_class = handler
        
        request_handler = handler_class()
        request_handler.initialize(self.request, self.response)
        
        if request_type == 'get':
          request_handler.get(*args)
        elif request_type == 'post':
          request_handler.post(*args)
        elif request_type == 'head':
          request_handler.head(*args)
        elif request_type == 'options':
          request_handler.options(*args)
        elif request_type == 'put':
          request_handler.put(*args)
        elif request_type == 'delete':
          request_handler.delete(*args)
        elif request_type == 'trace':
          request_handler.trace(*args)
        else:
          request_handler.error(501)
        
      elif inspect.isfunction(handler):
        handler_func = handler
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
        attrs[attr + '_action'] = attrs[attr]
        attrs[attr] = api_enabled(attrs[attr])
    
    return super(RequestHandlerMeta, cls).__new__(cls, name, bases, attrs)

class RequestHandler(webapp.RequestHandler):
  """docstring for RequestHandler"""
  __metaclass__ = RequestHandlerMeta
        
def get_handler_bindings():
  """docstring for get_handler_bindings"""
  pathes = router.get_all_pathes()
  return [(path, BaseHandler) for path in pathes]
