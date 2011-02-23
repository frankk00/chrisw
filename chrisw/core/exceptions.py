#!/usr/bin/env python
# encoding: utf-8
"""
exceptions.py

Created by Kang Zhang on 2011-02-15.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


class ChriswException(Exception):
  pass

class CannotResolvePath(ChriswException):
  """docstring for CannotResolvePath"""
  pass

class PermissionException(ChriswException):
  """docstring for PermissionError"""
  def __init__(self, msg, user, obj):
    super(PermissionError, self).__init__(msg)
    self.user = user
    self.obj = obj
