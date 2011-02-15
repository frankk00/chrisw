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

def register_path_handler(path, handler_method, handle_type):
  """docstring for register_url_handler"""
  global _handler_map
  _handler_map[path] = re.compile(path), handler_method, handle_type.lower()

def resolve_path(path, request_type):
  """docstring for route_url"""
  import logging
  logging.debug("request_type" + request_type)
  for path_reg, handler_method, handle_type in _handler_map.values():
    
    logging.debug("Resolve " + path + handle_type + request_type)
    if request_type == handle_type and path_reg.match(path):
      return handler_method
      
  return None

def get_all_pathes():
  """docstring for get_all_pathes"""
  return _handler_map.keys()