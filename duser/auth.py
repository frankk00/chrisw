#!/usr/bin/env python
# encoding: utf-8
"""
auth.py

The authentication libs

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

from gaesessions import get_current_session

from models import *

Guest = User(fullname="Guest", username="__GuestUserName", 
             email="guest@e.com", password="pwd")

def authenticate(username='', password=''):
  """Return a user object"""
  user = User.all().filter("username =", username.strip()) \
                   .filter("password =", password.strip()).get()
  return user

def get_current_user():
  """docstring for get_current_user"""
  session = get_current_session()
  
  logging.debug("Get current user, session %s", str(session))
  
  if session.has_key('current_user'):
    logging.debug("has current_user")
    return session['current_user']
  return Guest

def update_current_user(user):
  """docstring for update_current_user"""
  session = get_current_session()
  if session.has_key('current_user'):
    session['current_user'] = user

def login(user):
  """login the current user"""
  session = get_current_session()
  
  if session.is_active():
    session.terminate()
    
  session['current_user'] = user

def logout():
  """docstring for logout"""
  session = get_current_session()
  if session.is_active() and session.has_key('current_user'):
    user = session['current_user']
    user.put()
    
    session.terminate()



