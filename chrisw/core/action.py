#!/usr/bin/env python
# encoding: utf-8
"""
action.py

Created by Kang Zhang on 2011-02-18.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""
from chrisw.core import router
from chrisw.core.exceptions import *

class Action(object):
  """Base class for action"""
  def __init__(self):
    """docstring for __init__"""
    self.status = 'ok'

class back(Action):
  """docstring for back"""
  def __init__(self):
    super(back, self).__init__()

class login(Action):
  def __init__(self):
    super(login, self).__init__()

class template(Action):
  """docstring for template"""
  def __init__(self, name, var_dict):
    super(template, self).__init__()
    # strip the .html
    if name[-5:] == '.html': name = name[:-5]
    self.name = name
    self.var_dict = var_dict
  
  def render_to_string(self):
    """docstring for render"""
    from chrisw.helper.django_helper import render_to_string
    return render_to_string(self.name + ".html", self.var_dict)
    
class redirect(Action):
  """Redirect the user to page URL"""
  def __init__(self, to_url):
    super(redirect, self).__init__()
    self.to_url = to_url

class forward(Action):
  """forward action: load the content from the forwarding url.
  """
  def __init__(self, to_path, *args):
    super(forward, self).__init__()
    self.to_path = to_path
    self.args = args
    self.request_type = None
  
  def resolve_action(self):
    """Resolve the URL's action
    """
    
    
    path = self.to_path
    request_type = self.request_type
    handler = router.resolve_path(path, request_type)
    args = self.args
    action = None
    
    if handler:
      import inspect
      
      if inspect.isclass(handler):
        handler_class = handler
        
        request_handler = handler_class()
        # request_handler.initialize(self.request, self.response)
        
        if request_type == 'get':
          action = request_handler.get_action(*args)
        elif request_type == 'post':
          action = request_handler.post_action(*args)
        elif request_type == 'head':
          action = request_handler.head_action(*args)
        elif request_type == 'options':
          action = request_handler.options_action(*args)
        elif request_type == 'put':
          action = request_handler.put_action(*args)
        elif request_type == 'delete':
          action = request_handler.delete_action(*args)
        elif request_type == 'trace':
          action = request_handler.trace_action(*args)
        else:
          # use get as default
          action = request_handler.get_action(*args)
        
      elif inspect.isfunction(handler):
        handler_func = handler
        action = handler_func(self, *args)
        
    else:
      #exception happend  
      raise CannotResolvePath(path)
      
    return action
  
  def render_to_string(self):
    """docstring for render"""
    action = self.resolve_action()
    
    result_string = "Forward to PATH " + self.to_path 
    
    if action:
      if isinstance(action, template) or isinstance(action, forward):
        result_string = action.render_to_string()
      elif isinstance(action, redirect):
        result_string = "Redirect to " + action.to_url
      elif isinstance(action, login):
        result_string = "Login is required."
      elif isinstance(action, back):
        result_string = "Back to previous page."
      else:
        result_string = "Dose not support action " + str(action)
    else:
      pass
    
    return result_string
  
  def render(self):
    """docstring for evaluate"""
    return self.render_to_string()
    
    