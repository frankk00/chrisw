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
  func.request_type = 'get'
  return func

def Get(func, path):
  """docstring for get"""
  return request_handler(func, path, 'get')

def Post(func, path):
  """docstring for Post"""
  return request_handler(func, path, 'post')

def Options(func, path):
  """docstring for Options"""
  return request_handler(func, path, 'options')

def Head(func, path):
  """docstring for Head"""
  return request_handler(func, path, 'head')


