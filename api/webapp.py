#!/usr/bin/env python
# encoding: utf-8
"""
webapp.py

Created by Kang Zhang on 2010-09-26.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import sys
import os, logging

from google.appengine.ext import db

try:
  import json
except Exception, e:
  # before appengine's python upgrade to 2.7, we need import json from django
  from django.utils import simplejson as json


class PermissionError(Exception):
  """docstring for PermissionError"""
  def __init__(self, msg, user, obj):
    super(PermissionError, self).__init__()
    self.msg = msg
    self.user = user
    self.obj = obj
    
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
    
class PermissionUI(object):
  """docstring for PermissionModel"""
  def __init__(self, model_obj):
    super(PermissionModel, self).__init__()
    self.model_obj = model_obj
    self.user = get_current_user()
    
def view_method(func):
  """the target method is a view method, it returned 
      template_name, var_dict to be used by api_enabled decorator
  """
  def wrapper(self, *args, **kwargs):
    """docstring for wrapper"""
    
    template_name, var_dict = func(self, *args, **kwargs)
    # append the instance variable
    var_dict.update(self.__dict__)
    # skip the keys
    for key in ('self', 'model_obj'):
      del var_dict[key]
    
    return template_name, var_dict
    
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
    return 'template-name.html', varible_dict
  
  The return type of the handler can be
    1. template_name, var_dict . will be rendered with var_dict using template
      named template_name.
    2. new_url. will be directed to the new url.
    3. a exception raised from the method. will be wrapped with error:{}
  
  """
  
  def wrapper(self, *args, **kwargs):
    """docstring for wrapper"""
    
    result = func(self, *args, **kwargs)
    
    try:
      template, var_dict = result
    except Exception, e:
      logging.debug('Unsupported result for API call: %s', str(result))
      return result
    
    result_type = self.request.get('result_type', default_value="html")  
      
    if result_type == 'html':
      from django.shortcuts import render_to_response
      return self.response.out.write(render_to_response(template, var_dict))
    elif result_type == 'json':
      return self.response.out.write( var_dict )
      # return self.response.out.write(json.dumps(var_dict), skipkeys=True)
    
    pass
  
  return wrapper


def main():
	pass


if __name__ == '__main__':
	main()

