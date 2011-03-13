#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Created by Kang Zhang on 2011-03-11.
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

import logging
import unittest

from chrisw import db

from conf import settings
sys.path += settings.LIB_DIRS


def run_unittest():
  """docstring for run_unittest"""
  loader = unittest.defaultTestLoader
  
  suite = unittest.TestSuite()
  
  test_modules = []
  
  from tests.chrisw import test_db
  test_modules.append(test_db)
  from tests.common import test_models
  test_modules.append(test_models)
  
  print 'Start loading tests:' 
  for test_module in test_modules:
    print 'Loading test from %s ' % test_module.__name__
    suite.addTests(loader.loadTestsFromModule(test_module))
  
  print '%d Testsuites loaded.\n' % len(test_modules)
  print '-' * 70 
  unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)

def main():
  
  if not settings.DEBUG:
    print \
"""
*********************************************************************
              
              Kang Zhang (jobo.zh AT gmail.com) 

          Unittest could only be viewed in DEBUG model!

*********************************************************************
"""

  else:
    run_unittest()
  



if __name__ == '__main__':
	main()

