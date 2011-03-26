#!/usr/bin/env python
# encoding: utf-8
"""
decorators.py

Web decorators provides a easy way to register a method handler for a url. It
is much lightweight than classic ``RequestHandler``, but require the module to
be registered on application's init.

Usage:

  def topic_handler(func):
    # wrapper for all topic related hanlders, it retrieves topic model for 
    # request
    def wrapper(handler, topic_id):
      topic = GroupTopic.get_by_id(int(topic_id))
      topic_ui = TopicUI(topic)

      return func(topic_ui, handler.request)

    return wrapper

  @get_handler(r'/group/topic/(\d+)')
  @topic_handler
  def topic_view_get(topic_ui, request):
    return topic_ui.view(request)
  

More examples can be found in group/views/topicui.py

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
  """Decorator for get method
  
  Usage:
  @get_handler(r'/home')
  def home(self):
    return template('home_page')
  """
  return lambda func: request_handler(func, path, 'get')

def post_handler(path):
  """Decorator for post method"""
  return lambda func: request_handler(func, path, 'post')

def options_handler(path):
  """Decorator for options method"""
  return lambda func: request_handler(func, path, 'options')

def head_handler(path):
  """Decorator for head method"""
  return lambda func: request_handler(func, path, 'head')

def delete_handler():
  """Decorator for delete method"""
  return lambda func: request_handler(func, path, 'delete')

def trace_handler(path):
  """Decorator for trace method"""
  return lambda func: request_handler(func, path, 'trace')



