#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging
import settings
import os

from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms
from django import forms
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import blobstore_handlers

# import form fields
try:
  # for django 1.1
  from django.forms import CharField
  from django import forms as fields
except ImportError:
  # django 0.9
  from django.db import models as fields

from duser.auth import get_current_user

from duser import auth, User
from api.webapp import login_required, api_enabled, template, redirect
from api.shortcuts import render_to_string
from api.webapp import view_method, check_permission,PermissionUI
from api.shortcuts import render_to_string

from front.models import *

class UserForm(djangoforms.ModelForm):
  """docstring for UserForm"""
  class Meta:
    model = User
    fields = ["fullname", "password", "email"]

class ProfilePhotoForm(forms.Form):
  """docstring for ProfilePhoto"""
  photo = fields.ImageField(label="Profile Picture")
      
class UserUI(PermissionUI):
  """docstring for UserUI"""
  def __init__(self, user):
    super(UserUI, self).__init__(user)
    self.user = user
  
  @view_method
  @check_permission("view", "Can't view the user's profile")
  def view(self):
    """the view of user profile"""
    return None
  
  # every user can only see his/her own setting page, don't need check
  # the permission
  @view_method
  def profile(self):
    """The user profile settings page"""
    form = UserForm(data=self.user.to_dict())
    photo_form = ProfilePhotoForm()
    from google.appengine.ext import blobstore
    photo_upload_url = blobstore.create_upload_url('/u/avatar/upload')
    return template('user_profile', locals())
  
  # same to the previous method
  def profile_post(self, request):
    """docstring for edit_post"""
    pass
  

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
  @api_enabled
  def get(self):
    userui = UserUI(get_current_user())
    return userui.profile()
    
  @api_enabled
  def post(self):
    userui = UserUI(get_current_user())
    return userui.profile_post()

class UserProfilePhotoHandler(blobstore_handlers.BlobstoreUploadHandler):
  
  @api_enabled
  def post(self):
    upload_files = self.get_uploads()  # 'file' is file upload field in the form
    
    if not upload_files:
      return redirect('/u/profile')
    
    blob_info = upload_files[0]
    
    user = get_current_user()
    
    logging.debug(" Got user %s 's avatar %d", user.username, blob_info.size)
    if user and blob_info.size <= 1024 * 100:
      
      from google.appengine.api import images
      
      user.photo_url = images.get_serving_url(str(blob_info.key()))
      user.photo_blob_key = str(blob_info.key())
      user.put()
      
      logging.debug("New profile url: " + user.photo_url)
      
      return redirect('/u/profile')
    else:
      blob_info.delete()
      import errors
      raise errors.Error("File is too large")
  
apps = [(r'/u/(\d+)', UserProfileHandler),
        (r'/u/profile', UserProfileSettingHandler),
        (r'/u/avatar/upload', UserProfilePhotoHandler),
        ]
    
