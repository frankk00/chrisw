#!/usr/bin/env python
# encoding: utf-8
"""
webapp.py

Created by Kang Zhang on 2010-09-26.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import sys
import os, logging

try:
  import json
except Exception, e:
  # before appengine's python upgrade to 2.7, we need import json from django
  from django.utils import simplejson as json


def api_enabled(func):
  """docstring for api_enabled"""
  
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

