#!/usr/bin/env python
# encoding: utf-8
"""
auth.py

Created by Kang Zhang on 2011-02-17.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


from gaesessions import get_current_session

def get_current_user(default_user=None):
  """Return the current logined user.
  
  Optional default_user will be returned if the user has not been logined.
  """
  session = get_current_session()
  
  if session.has_key('current_user'):
    try:
      return session['current_user']
    except Exception, e:
      pass
    
  return default_user

def update_current_user(user):
  """Update current user model"""
  session = get_current_session()
  if session.has_key('current_user'):
    session['current_user'] = user

def login(user):
  """Login the given user"""
  session = get_current_session()
  
  if session.is_active():
    session.terminate()
    
  session['current_user'] = user

def logout():
  """Logout current user"""
  session = get_current_session()
  if session.is_active() and session.has_key('current_user'):
    user = session['current_user']
    user.put()
    
    session.terminate()



