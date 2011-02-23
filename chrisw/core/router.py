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

_handler_map = {}

def register_path_handler(path, handler, handle_type):
  """Regiester a handler for a path, the handler could be a handler method or
  a handler class. 
  """
  global _handler_map
  _handler_map[path] = re.compile(path), handler, handle_type.lower()

def resolve_path(path, request_type):
  """request_type could
  """
  
  for path_reg, handler, handle_type in _handler_map.values():
    
    if request_type == handle_type and path_reg.match(path):
      return handler
      
  return None

def get_all_pathes():
  """docstring for get_all_pathes"""
  return _handler_map.keys()