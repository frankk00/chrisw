#!/usr/bin/env python
# encoding: utf-8
"""
filters.py

Created by Kang Zhang on 2010-10-11.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from django import template

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
