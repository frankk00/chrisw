#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import blobstore_handlers


from api.helpers import fields, forms

from api.webapp import login_required, api_enabled, template, redirect
from api.webapp import view_method, check_permission,PermissionUI
from api.shortcuts import render_to_string

from duser.auth import get_current_user
from duser import auth, User
from front.models import *
from group.models import UserGroupInfo
from conf import settings
from api.i18n import _
import photo

class UserForm(djangoforms.ModelForm):
  """docstring for UserForm"""
  class Meta:
    model = User
    fields = ["fullname", "email", "status_message"]
  
  fullname = fields.CharField(label = _('Full Name'), min_length=1,\
    max_length=10)
  status_message = fields.CharField(label = _("Status Message"), min_length=1,\
    max_length=70)
  email = fields.EmailField(label = _('Email'))

class ProfilePhotoForm(forms.Form):
  """docstring for ProfilePhoto"""
  photo = fields.ImageField(label = _("Profile Picture"))
      
class UserUI(PermissionUI):
  """docstring for UserUI"""
  def __init__(self, user):
    super(UserUI, self).__init__(user)
    self.user = user
  
  @view_method
  @check_permission("view", "Can't view the user's profile")
  def view(self):
    """the view of user profile"""
    groupinfo = UserGroupInfo.get_by_user(self.user)
    joined_groups = db.get(groupinfo.groups)
    is_login_user = self.user.key() == get_current_user().key()
    
    return template('user_home', locals())
  
  # every user can only see his/her own setting page, don't need check
  # the permission
  @view_method
  @check_permission("edit", "Cant't edit the user's profile")
  def profile(self, request):
    """The user profile settings page"""
    
    # user image setting
    if request.get('image_url', ''):
      self.user.photo_url = request.get('image_url')
      self.user.put()
    
    form = UserForm(data=self.user.to_dict())
    photo_form = ProfilePhotoForm()
    photo_upload_url = photo.create_upload_url()
    back_url = request.path
    
    logging.debug("form %s", self.user.to_dict())
    
    return template('user_profile', locals())
  
  # same to the previous method
  @view_method
  @check_permission("edit", "Can't edit the user's profile")
  def profile_post(self, request):
    """docstring for edit_post"""
    form = UserForm(data=request.POST, instance=self.user)
    if form.is_valid():
      user = form.save(commit=False)
      user.put()
      
      redirect('u/profile')
    
    # redraw the settings page
    photo_form = ProfilePhotoForm()
    photo_upload_url = photo.create_upload_url()
    back_url = request.path
      
    return template('user_profile', locals())
  

class UserHandler(webapp.RequestHandler):
  """docstring for UserHandler"""
  
  def get_impl(self, userui):
    """docstring for get_impl"""
    raise Exception("Not implemented yet")
  
  def post_impl(self, userui, request):
    """docstring for post_impl"""
    return self.get_impl(userui)
  
  @api_enabled
  def get(self, userid):
    """docstring for get"""
    logging.debug("Hello world")
    user = User.get_by_id(int(userid))
    return self.get_impl(UserUI(user))
  
  @api_enabled
  def post(self, userid):
    """docstring for post"""
    user = User.get_by_id(int(userid))
    return self.post_impl(UserUI(user))
    

class UserProfileHandler(UserHandler):
  """docstring for UserProfileHandler"""
  def get_impl(self, userui):
    return userui.view()
  
class UserProfileSettingHandler(webapp.RequestHandler):
  """docstring for UserSettingHandler"""
  @login_required
  @api_enabled
  def get(self):
    userui = UserUI(get_current_user())
    return userui.profile(self.request)
  
  @login_required
  @api_enabled
  def post(self):
    userui = UserUI(get_current_user())
    return userui.profile_post(self.request)
    
  
apps = [(r'/u/(\d+)', UserProfileHandler),
        (r'/u/profile', UserProfileSettingHandler),
        ]
    
