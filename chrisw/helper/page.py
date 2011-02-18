#!/usr/bin/env python
# encoding: utf-8
"""
Page.py

Created by Kang Zhang on 2011-02-18.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

class Page(object):
  """docstring for Paginator"""
  def __init__(self, request, offset, limit, count):
    super(Page, self).__init__()
    self.count = count
    self.offset = offset
    self.limit = limit
    self.request = request
    self.page_size = limit - offset
    self.path = request.path
  
  def has_next(self):
    """docstring for has_next"""
    return self.limit < self.count
  
  def has_prev(self):
    """docstring for has_previous"""
    return self.offset != 0
  
  def prev_page(self):
    """docstring for prev_page"""
    return Page(self.request, self.offset - self.page_size, \
      self.limit - self.page_size, self.count)
  
  def next_page(self):
    """docstring for next_page"""
    return Page(self.request, self.offset + self.page_size, \
      self.limit + self.page_size, self.count)
  
  def next_url(self):
    """docstring for next_url"""
    
    logging.debug("URL: " + self.url())
    return self.next_page().url() 
  
  def prev_url(self):
    """docstring for prev_url"""
    return self.prev_page().url()
  
  def url(self):
    """docstring for url"""
    # logging.debug("URL: " + self.path + "?offset=" + self.offset + "&limit=" + self.limit)
    return self.path + "?offset=" + str(self.offset) + "&limit=" + \
      str(self.limit)