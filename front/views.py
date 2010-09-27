#!/usr/bin/env python
# encoding: utf-8
"""
views.py

Created by Kang Zhang on 2010-09-22.
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
from api.webapp import login_required, api_enabled, template, redirect
from api.shortcuts import render_to_string

class MainHandler(webapp.RequestHandler):
  def get(self):
    # path = os.path.join(os.path.dirname(__file__), '../templates/base.html')
    # self.response.out.write(template.render(path, {'user': 'andyzhau'}))
    self.response.out.write(render_to_string('base.html', {'user': 'andyzhau'}))

def create_login_url(url):
  """docstring for create_login_url"""
  import urllib
  back_url = urllib.quote_plus(url)
  return settings.LOGIN_URL + "?back_url=" + back_url

class FrontPageHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write('Hello world! ')

class RegForm(djangoforms.ModelForm):
  class Meta:
    model = auth.User
    fields = ['username', 'uid', 'password', 'email']
  username = fields.CharField()
  
  def is_valid(self):
    """docstring for is_valid"""
    if super(djangoforms.ModelForm, self).is_valid():
      uid = self.data.get('uid')
      if uid and auth.User.gql("WHERE uid=:uid ", uid=uid).get() == None:
        return True
      else:
        self.errors['uid'] = ['Username %s exists already' % uid]
    return False
  
class SignupUserHanlder(webapp.RequestHandler):
  """docstring for RegUserHanlder"""
  @api_enabled
  def get(self):
    """default sign up page"""
    form = RegForm()
    return template('signin.html', locals())
  
  @api_enabled
  def post(self):
    """docstring for post"""
    form = RegForm(data=self.request.POST)
    if form.is_valid():
      new_user = form.save(commit=False)
      new_user.put()
      return template('signin_successful.html', locals())
    else:
      return template('signin.html', locals())

class LoginForm(forms.Form):
  """docstring for LoginForm"""
  uid = fields.CharField()
  password = fields.CharField()
  
  def is_valid(self):
    """docstring for is_valid"""
    if super(forms.Form, self).is_valid():
      uid = self.data['uid']
      password = self.data['password']
      
      self.user = auth.authenticate(uid, password)
      if self.user: 
        return True
      else:
        self.errors['username'] = ['Wrong username or password']
    return False
      
class LoginUserHandler(webapp.RequestHandler):
  """docstring for LoginHandler"""
  @api_enabled
  def get(self):
    """docstring for get"""
    form = LoginForm()
    page_url = self.request.path + "?" + self.request.query_string
    return template('login.html', locals())
  
  @api_enabled
  def post(self):
    """docstring for post"""
    form = LoginForm(data=self.request.POST)
    if form.is_valid():
      auth.login(form.user)
      back_url = self.request.get('back_url')
      if back_url:
        return redirect(back_url)
      else:
        return template('login_successful.html', locals())
    else:
      return template('login.html', locals())
    
class LoginDemoHandler(webapp.RequestHandler):
  """docstring for ClassName"""
  @login_required
  def get(self):
    import gaesessions
    logging.debug("current session %s", gaesessions.get_current_session())
    self.response.out.write(render_to_string('test_login.html', locals()))
    