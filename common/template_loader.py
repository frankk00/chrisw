#!/usr/bin/env python
# encoding: utf-8
"""
template_loader.py

Created by Kang Zhang on 2011-04-09.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

# config the django's settings, is needed by django 1.1 but not 0.96
# explain from django's doc:
#   It boils down to this: Use exactly one of either configure() or 
#   DJANGO_SETTINGS_MODULE. Not both, and not neither.
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'conf.settings'

# patch from google
# refer to http://code.google.com/appengine/docs/python/tools/libraries.html#Django
from google.appengine.dist import use_library
use_library('django', '1.2')

import sys
import os

from conf import settings

from google.appengine.ext import webapp

from chrisw.core import handlers
from chrisw.core.action import text

_LEFT_BRACE_ = '_LEFT_BRACE_'
_RIGHT_BRACE_ = '_RIGHT_BRACE_'

def minimize(template):
  """docstring for minimize"""
  
  from django.template import Template, Context
  
  # leave {{ for mustache
  template = template.replace('{{', _LEFT_BRACE_).replace(_RIGHT_BRACE_, '}}')
  
  template = Template(template).render(Context({}))
  
  template = template.replace(_LEFT_BRACE_, '{{').replace(_RIGHT_BRACE_, '}}')
  
  return template.replace('\n', '').replace("'","\\'")

def generate_script():
  
  template_names = ['user_stream_reply']
  
  template_folder = os.path.join(os.path.dirname(__file__), 'templates')
  
  template_pairs = []
  for template_name in template_names:
    template_path = os.path.join(template_folder, "js_" + template_name + ".html")
    template = minimize(open(template_path).read())
    template_pairs.append("%s :'%s'" % (template_name, template))
  
  template_pair_string = "\n".join(template_pairs)
  
  script_formats = """
  chrisw.templates = {
    %s 
  }"""
  
  script = script_formats % template_pair_string
  
  return script

class MainPage(handlers.RequestHandler):
  
  def get(self):
    return text(generate_script())

application = webapp.WSGIApplication([('/javascript/templates.js', MainPage)],
                                     debug=True)

def main():
    from google.appengine.ext.webapp.util import run_wsgi_app
    run_wsgi_app(application)


if __name__ == '__main__':
  main()

