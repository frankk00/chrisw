#!/usr/bin/env python
# encoding: utf-8
"""
action.py

Created by Kang Zhang on 2011-02-18.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""
from chrisw.core import router, memcache
from chrisw.core.exceptions import *

class Action(object):
  """Base class for action"""
  def __init__(self):
    """docstring for __init__"""
    self.status = 'ok'

class back(Action):
  """``back`` action: return to the previous page"""
  def __init__(self):
    super(back, self).__init__()

class login(Action):
  """``login`` action: return to the login page"""
  def __init__(self):
    super(login, self).__init__()

class _RenderAction(Action):
  """The base action for all rendering related actions"""
  def render_to_string(self):
    """render content to string"""
    raise Exception('Not implemented method')

class template(_RenderAction):
  """``template`` action: render the string using the given template."""
  def __init__(self, name, var_dict):
    super(template, self).__init__()
    # strip the .html
    if name[-5:] == '.html': name = name[:-5]
    self.name = name
    self.var_dict = var_dict
  
  def render_to_string(self):
    
    # add always needed info
    var_dict = self.var_dict
    # add login info
    from common.auth import get_current_user, Guest
    user = get_current_user()
    user_info = {'login_user':user, 'is_not_guest':user != Guest}
    var_dict.update(user_info)
    
    from home.models import Site
    site_info = {'site':Site.get_instance()}
    var_dict.update(site_info)
    
    from chrisw.helper.django_helper import render_to_string
    return render_to_string(self.name + ".html", self.var_dict)

class text(_RenderAction):
  """docstring for text"""
  def __init__(self, _text):
    super(text, self).__init__()
    self._text = _text
  
  def render_to_string(self):
    """docstring for render_to_string"""
    return self._text
    
class redirect(Action):
  """Redirect the user to page URL"""
  def __init__(self, to_url):
    super(redirect, self).__init__()
    self.to_url = to_url

class cache(_RenderAction):
  """``cache`` action, which is used to cache the render result string"""
  def __init__(self, func, func_args, func_kwargs, key, time=60):
    super(cache, self).__init__()
    self.key = key
    self.time = time
    self.func = func
    self.func_args = func_args
    self.func_kwargs = func_kwargs
  
  def render_to_string(self):
    data = memcache.get(self.key)
    if data is not None:
      import logging
      logging.debug("cache hitted for key: %s", self.key)
      return data
    
    action = self.func(*self.func_args, **self.func_kwargs)
    
    if not isinstance(action, _RenderAction) or isinstance(action, cache):
      raise Exception("Can't cache the action except template and forward")
      
    data = action.render_to_string()
    memcache.set(self.key, data, self.time)
    return data
    

class forward(_RenderAction):
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
    action = self.resolve_action()
    
    result_string = "Forward to PATH " + self.to_path 
    
    if action:
      if isinstance(action, _RenderAction):
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
      result_string += " Can't resolve the forwared action"
    
    return result_string
  
  def render(self):
    """Retrieve the fowarded content"""
    return self.render_to_string()
    
    