#!/usr/bin/env python
# encoding: utf-8
"""
util.py

Created by Kang Zhang on 2011-02-15.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

import sys
import logging
import inspect

from chrisw.core import router

from decorators import *

def register_app(app_names):
  """docstring for register_app"""
  module_names = []
  
  for app_name in app_names:
    view_module_name = app_name + "." + "views"
    module_names.append(view_module_name)
  
  for module_name in module_names:
    try:
      __import__(module_name, globals(), locals())
      module = sys.modules[module_name]
      members = [module.__dict__[m] for m in dir(module)]
      submodules = [m for m in members if inspect.ismodule(m)]
      
      for submodule in submodules:
        smembers = [submodule.__dict__[m] for m in dir(submodule)]
        sfunctions = [m for m in smembers if inspect.isfunction(m)]

        for func in sfunctions:
          if hasattr(func,'is_request_handler') and func.is_request_handler:
            path = func.path
            request_type = func.request_type
            
            router.register_path_handler(path, func, request_type)
            
    except ImportError, e:
      logging.error("Can't import " + module_name)

def run_appengine_app():
  """docstring for run_appengine_app"""
  
  from google.appengine.ext.webapp.util import run_wsgi_app
  from google.appengine.ext import webapp
  from chrisw.core import handlers
  
  application = webapp.WSGIApplication(handlers.get_handler_bindings(),\
                                       debug=True)
  run_wsgi_app(application)
  
  
    