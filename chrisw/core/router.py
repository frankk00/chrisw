#!/usr/bin/env python
# encoding: utf-8
"""
router.py

Created by Kang Zhang on 2011-02-15.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

"""
We don't use url here. We use the path of the URL instead, i.e. the string
between the host name and the query parameters.
"""


import re
import logging
import inspect

from chrisw.core import exceptions

_handler_map = {}

class NotSupportedHandlerException(exceptions.Exception):
  """docstring for NotSupportedHandlerException"""
  def __init__(self, handler):
    super(NotSupportedHandlerException, self).__init__()
    self.reason = "Handler is neither class nor function " + str(handler)
    

def register_path_handler(path, handler, handle_type = None):
  """Regiester a handler for a path, the handler could be a handler method or
  a handler class. 
  """
  global _handler_map
  
  if _handler_map[path]:
    logging.warning("Duiplicated handler has been specified for URL: %s", path)
  
  if handle_type:
    handle_type = handle_type.lower()
  
  if not inspect.isclass(handler) and not inspect.isclass(handler):
    raise NotSupportedHandlerException(handler)
    
  _handler_map[path] = re.compile(path), handler, handle_type

def resolve_path(path, request_type = None):
  """request_type could be None to just get the handler 
  """
  
  for path_reg, handler, handle_type in _handler_map.values():
    
    if not request_type or (request_type == handle_type and \
      path_reg.match(path)):
      
      return handler
      
  return None

def get_all_pathes():
  """docstring for get_all_pathes"""
  return _handler_map.keys()