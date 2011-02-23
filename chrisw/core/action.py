#!/usr/bin/env python
# encoding: utf-8
"""
action.py

Created by Kang Zhang on 2011-02-18.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


class Action(object):
  """Base class for action"""
  def __init__(self):
    """docstring for __init__"""
    self.status = 'ok'

class back(Action):
  """docstring for back"""
  def __init__(self):
    super(back, self).__init__()

class login(Action):
  def __init__(self):
    super(login, self).__init__()

class template(Action):
  """docstring for template"""
  def __init__(self, name, var_dict):
    super(template, self).__init__()
    # strip the .html
    if name[-5:] == '.html': name = name[:-5]
    self.name = name
    self.var_dict = var_dict
  
  def render_to_string(self):
    """docstring for render"""
    from chrisw.helper.django_helper import render_to_string
    return render_to_string(self.name + ".html", self.var_dict)
    
class redirect(Action):
  """Redirect the user to page URL"""
  def __init__(self, to_url):
    super(redirect, self).__init__()
    self.to_url = to_url

class forward(Action):
  """forward action: load the content from the forwarding url.
  """
  def __init__(self, to_url, var_dict = {}):
    super(forward, self).__init__()
    self.to_url = to_url
    self.var_dict = var_dict
  
  def render(self):
    """docstring for render"""
    pass