#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from google.appengine.api import users
from chrisw import db
from common import models as ndb
from conf import settings

class User(ndb.Entity):
  """docstring for User"""
  fullname = db.StringFlyProperty(required=True)
  username = db.StringProperty(required=True)
  create_date = db.DateTimeProperty(auto_now_add=True)
  password = db.StringProperty(required=True)
  email = db.EmailProperty(required=True)
  status_message = db.StringFlyProperty(default="")
  photo_url = db.StringFlyProperty(default=settings.DEFAULT_USER_PHOTO)
  
  def can_visit_key(self, user, key):
    """Privacy control, protect ur privacy here"""
    if key == 'password':
      return False
    elif key == 'email':
      # can be visible by the user himself
      return user and user.username == self.username
    return True
    
  def change_to_gravatar_icon(self):
    """docstring for change_to_gravatar"""
    # use gravatar icon
    import hashlib
    self.photo_url = settings.GRAVATAR_BASE + \
      str(hashlib.md5(self.email.lower()).hexdigest()) + "?d=identicon&s=48"
  
  def put(self):
    """User could be built from sessions, need write through these users"""
    from auth import get_current_user, update_current_user
    
    user = get_current_user()
    
    if user and user.username == self.username:
      update_current_user(self)
    
    super(User, self).put()
    
  def can_view(self, user):
    """docstring for can_view"""
    return True
    
  def can_edit(self, user):
    """docstring for can_edit"""
    return self.key() == user.key()
  
  def full_photo(self):
    """docstring for full_photo"""
    return self.photo_url


Guest = User.all().filter('username =', "__GuestUserName").get()

if not Guest:
  Guest = User(fullname="Guest", username="__GuestUserName", 
             email="guest@chrisw", password="pwd")
  db.put(Guest)