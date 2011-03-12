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


def main():
  
  suite = unittest.TestSuite()
  
  from tests.chrisw import test_db
  suite.addTests(test_db.suite)
  
  from tests.common import test_models
  suite.addTests(test_models.suite)
  
  unittest.TextTestRunner(verbosity=2).run(suite)
  pass


if __name__ == '__main__':
	main()

