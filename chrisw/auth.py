#!/usr/bin/env python
# encoding: utf-8
"""
auth.py

Created by Kang Zhang on 2011-02-17.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


from gaesessions import get_current_session

def get_current_user(default_user=None):
  """docstring for get_current_user"""
  session = get_current_session()
  
  if session.has_key('current_user'):
    return session['current_user']
    
  return default_user

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



