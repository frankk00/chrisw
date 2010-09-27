#!/usr/bin/env python
# encoding: utf-8
"""
webapp.py

Created by Kang Zhang on 2010-09-26.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import sys
import os, logging

import errors

from google.appengine.ext import db

from duser.auth import get_current_user

try:
  import json
except Exception, e:
  # before appengine's python upgrade to 2.7, we need import json from django
  from django.utils import simplejson as json

class Action(object):
  """Base class for action"""
  pass

class template(Action):
  """docstring for template"""
  def __init__(self, name, var_dict):
    super(template, self).__init__()
    # strip the .html
    if name[-5:] == '.html': name = name[:-5]
    self.name = name
    self.var_dict = var_dict
    
class redirect(Action):
  """Redirect the user to page URL"""
  def __init__(self, to_url):
    super(redirect, self).__init__()
    self.to_url = to_url

class check_permission(object):
  """docstring for check_permission"""
  def __init__(self, action, error_msg):
    super(check_permission, self).__init__()
    self.action = action
    self.error_msg = error_msg

  def __call__(self, func):
    """docstring for __call__"""
    def wrapper(ui, *args, **kwargs):
      """docstring for wrapper"""
      f = getattr(ui.model_obj, 'can_' + self.action)

      if f(ui.user):
        return func(ui, *args, **kwargs)
      raise PermissionError(error_msg, ui.user, ui.model_obj)

    return wrapper  

class PermissionError(errors.Error):
  """docstring for PermissionError"""
  def __init__(self, msg, user, obj):
    super(PermissionError, self).__init__(msg)
    self.user = user
    self.obj = obj

class APIError(errors.Error):
  """docstring for APIError"""
  def __init__(self, reason):
    super(APIError, self).__init__(reason)
    self.reason = reason

def login_required(func):
  """
  Usage:
  @login_required
  def post(self):
    pass
  """
  from duser.auth import get_current_user

  def wrapper(self, *args, **kwargs):
    """docstring for wrapper"""

    if get_current_user():
      return func(self, *args, **kwargs)
    else:
      import front
      return self.redirect(front.create_login_url(self.request.url))

  return wrapper

    
class PermissionUI(object):
  """docstring for PermissionModel"""
  def __init__(self, model_obj):
    super(PermissionUI, self).__init__()
    
    if not model_obj:
      raise APIError("Can't find item. Wrong ID?")
    
    self.model_obj = model_obj
    self.user = get_current_user()
    
def view_method(func):
  """the target method is a view method, it returned 
      template_name, var_dict to be used by api_enabled decorator
  """
  def wrapper(self, *args, **kwargs):
    """docstring for wrapper"""
    
    action = func(self, *args, **kwargs)
    # append the instance variable
    if hasattr(action, 'var_dict'):
      var_dict = action.var_dict
      var_dict.update(self.__dict__)
      # skip the keys
      for key in ('self', 'model_obj'):
        del var_dict[key]
    
    return action
    
  return wrapper

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
    
    try:
      action = func(self, *args, **kwargs)
      
      if isinstance(action, redirect):
        var_dict = {'redirect':action.to_url}
      elif isinstance(action, template):
        var_dict = action.var_dict
        
    except errors.Error as e:
      action, var_dict = template('error.html'), dict({'error':e.msg})
      
    if result_type == 'html':
      
      if isinstance(action, redirect):
        # redirect action
        return self.redirect(action.to_url)
        
      # template action
      from shortcuts import render_to_string
      return self.response.out.write(render_to_string(action.name + '.html', var_dict))
    elif result_type == 'json':
      return self.response.out.write(var_dict)
  
  return wrapper


