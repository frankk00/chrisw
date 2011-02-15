#!/usr/bin/env python
# encoding: utf-8
"""
decorators.py

Created by Kang Zhang on 2011-02-15.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

def request_handler(func, path, request_type = 'get'):
  """docstring for request_handler"""
  func.is_request_handler = True
  func.path = path
  func.request_type = request_type
  return func

def get_handler(path):
  """docstring for get"""
  return lambda func: request_handler(func, path, 'get')

def post_handler(path):
  """docstring for Post"""
  return lambda func: request_handler(func, path, 'post')

def options_handler(path):
  """docstring for Options"""
  return lambda func: request_handler(func, path, 'options')

def head_handler(path):
  """docstring for Head"""
  return lambda func: request_handler(func, path, 'head')


