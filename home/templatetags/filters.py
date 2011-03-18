#!/usr/bin/env python
# encoding: utf-8
"""
filters.py

Created by Kang Zhang on 2010-10-11.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""
from django import template
from chrisw.i18n import _

register = template.Library()

@register.filter
def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.
    
    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
        
    Note: this snippet is get from the web:
    http://djangosnippets.org/snippets/1259/
    
    """
    
    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value
    
    # Make sure it's unicode
    value = unicode(value)
    
    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value
    
    # Cut the string
    value = value[:limit]
        
    # Break into words and remove the last
    words = value.split(' ')[:-1]
    if not words:
      words = (value,)
    
    # Join the words and return
    return ' '.join(words) + '...'


@register.filter
def pretty_time(time):
  """
  Get a datetime object or a int() Epoch timestamp and return a
  pretty string like 'an hour ago', 'Yesterday', '3 months ago',
  'just now', etc
  
  This method derived from the stackover flow post:
  
    http://stackoverflow.com/questions/1551382/python-user-friendly-time-format
  """
  from datetime import datetime
  now = datetime.now()
  if type(time) is int:
    diff = now - datetime.fromtimestamp(time)
  elif not time:
    diff = now - now
  else:
    diff = now - time
  second_diff = diff.seconds
  day_diff = diff.days
  
  if day_diff < 0:
    return ''
  
  if day_diff == 0:
    if second_diff < 10:
        return _("just now")
    if second_diff < 60:
      return str(second_diff) + _(" seconds ago")
    if second_diff < 120:
      return  "a minute ago"
    if second_diff < 3600:
      return str( second_diff / 60 ) + _(" minutes ago")
    if second_diff < 7200:
      return "an hour ago"
    if second_diff < 86400:
      return str( second_diff / 3600 ) + _(" hours ago")
        
  if day_diff == 1:
      return "Yesterday"
  if day_diff < 7:
      return str(day_diff) + _(" days ago")
  if day_diff < 31:
      return str(day_diff/7) + _(" weeks ago")
  if day_diff < 365:
      return str(day_diff/30) + _(" months ago")
      
  return str(day_diff/365) + _(" years ago")
  