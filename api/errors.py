#!/usr/bin/env python
# encoding: utf-8
"""
errors.py

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

class Error(Exception):
  """docstring for DException"""
  def __init__(self, msg):
    super(Error, self).__init__()
    self.msg = msg
        
