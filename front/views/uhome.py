#!/usr/bin/env python
# encoding: utf-8
"""
uhome.py

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

# import form fields
try:
  # for django 1.1
  from django.forms import CharField
  from django import forms as fields
except ImportError:
  # django 0.9
  from django.db import models as fields

from duser import auth
from duser.auth import get_current_user
from api.webapp import login_required, api_enabled, template, redirect
from api.webapp import view_method, check_permission,PermissionUI
from api.shortcuts import render_to_string

from front.models import UHome

class LoginForm(forms.Form):
  """docstring for LoginForm"""
  username = fields.CharField()
  password = fields.CharField(widget=forms.PasswordInput)
  
  def is_valid(self):
    """docstring for is_valid"""
    if super(forms.Form, self).is_valid():
      username = self.data['username']
      password = self.data['password']
      
      if auth.authenticate(username, password): return True # success
      # Wrong password
      else: self.errors['username'] = ['Wrong username or password']
      
    return False

class RegForm(djangoforms.ModelForm):
  class Meta:
    model = auth.User
    fields = ['fullname', 'username', 'password', 'email']
    
  fullname = fields.CharField(label='Full name', min_length=6, max_length=30)
  username = fields.CharField(min_length=5, max_length=30)
  password = fields.CharField(widget=forms.PasswordInput, min_length=4, 
                              max_length=30)
  email = fields.EmailField()
  
  def is_valid(self):
    """docstring for is_valid"""
    if super(djangoforms.ModelForm, self).is_valid():
      username = self.data.get('username')
      self.user = auth.User.all().filter("username =",username).get()
      if username and self.user == None: 
        return True
      # can't regieser as user name
      else: self.errors['username'] = ['Username %s exists already' % username]
      
    return False
    
class UHomeUI(PermissionUI):
  """docstring for UHomeUI"""
  def __init__(self, uhome = UHome()):
    super(UHomeUI, self).__init__(uhome)
    self.uhome = uhome
  
  @view_method
  def login(self, request):
    """docstring for login"""
    form = LoginForm()
    page_url = request.path + "?" + request.query_string
    return template('login.html', locals())
  
  @view_method
  def login_post(self, request):
    """The post handler for user login"""
    form = LoginForm(data=request.POST)
    user = auth.get_current_user()
    if form.is_valid():
      auth.login(form.user)
      back_url = request.get('back_url', '/')
      if back_url:
        return redirect(back_url)
      else:
        return template('login_successful.html', locals())
    else:
      return template('login.html', locals())
  
  @view_method
  def logout(self):
    """docstring for logout"""
    auth.logout()
    return redirect("/")
  
  @view_method
  def signup(self):
    """The user sign up page"""
    form = RegForm()
    return template('signup.html', locals())
  
  @view_method
  def signup_post(self, request):
    """The post handler for user signup"""
    form = RegForm(data=request.POST)
    if form.is_valid():
      new_user = form.save(commit=False)
      new_user.put()
      return template('signup_successful.html', locals())
    else:
      return template('signup.html', locals())

class UHomeHandler(webapp.RequestHandler):
  """docstring for UHomeHandler"""
  
  def get_impl(self, uhomeui):
    """docstring for get_impl"""
    raise Exception("did not implemented")
  
  def post_impl(self, uhomeui, request):
    """docstring for post_imple"""
    return self.get_impl(uhomeui)
  
  @api_enabled
  def get(self):
    """docstring for get"""
    uhomeui = UHomeUI()
    return self.get_impl(uhomeui)
  
  @api_enabled
  def post(self):
    """docstring for post"""
    uhomeui = UHomeUI()
    return self.post_impl(uhomeui, self.request)

class SignupUserHanlder(UHomeHandler):
  """docstring for RegUserHanlder"""
  def get_impl(self, uhomeui):
    return uhomeui.signup()
  
  def post_impl(self, uhomeui, request):
    return uhomeui.signup_post(request)
      
class LoginUserHandler(UHomeHandler):
  """docstring for LoginHandler"""
  def get_impl(self, uhomeui):
    return uhomeui.login(self.request)
  
  def post_impl(self, uhomeui, request):
    return uhomeui.login_post(request)

class LogoutUserHandler(UHomeHandler):
  """docstring for LogoutUserHandler"""
  def get_impl(self, uhomeui):
    return uhomeui.logout()

class LoginDemoHandler(UHomeHandler):
  """docstring for ClassName"""
  @login_required
  def get(self):
    import gaesessions
    logging.debug("current session %s", gaesessions.get_current_session())
    self.response.out.write(render_to_string('test_login.html', locals()))

apps = [('/signup', SignupUserHanlder),
        # since loging url is needed to do authentication
        (settings.LOGIN_URL, LoginUserHandler),
        ('/logout', LogoutUserHandler),
        ('/test_login', LoginDemoHandler),]
