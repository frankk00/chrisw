#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import groupui
import topic

apps = groupui.apps + topic.apps


from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms

from duser.auth import get_current_user
from api.webapp import login_required, api_enabled
from api.webapp import check_permission, view_method, PermissionUI
from google.appengine.ext import webapp
class NewItemHandler(webapp.RequestHandler):
  """docstring for NewItemHandler"""
  
  def create_form(self, *args):
    """docstring for create_item"""
    raise Exception("Has not been implementation")
    
  def template_name(self):
    """docstring for template_name"""
    raise Exception("Has not been implementation")
  
  @login_required
  @api_enabled
  def get(self):
    """docstring for get"""
    form = self.create_form()
    return self.template_name(), locals()
  
  @login_required
  @api_enabled
  def post(self):
    """docstring for post"""
    form = self.create_form(data = self.request.POST)
    if form.is_valid():
      logging.debug("want to save group")
      group = form.save(commit=False)
      group.create_user = get_current_user()
      group.put()
    
    return self.template_name(), locals()


class NewGroupHandler(NewItemHandler):
  """docstring for CreateGroupHandler"""
  
  def create_form(self, *args):
    return GroupForm(*args)
    
  def template_name(self):
    return 'item_new.html'

class NewTopicHandler(NewItemHandler):
  def create_form(self, *args):
    """docstring for create_form"""
    return TopicForm(*args)
  
  def template_name(self):
    """docstring for template_name"""
    return 'item_new.html'


    



