#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

from google.appengine.api import users
from chrisw import db, gdb
from chrisw.core.memcache import cache_result
from conf import settings

class User(gdb.Entity):
  """docstring for User"""
  fullname = db.StringProperty(required=True, default="Name")
  username = db.StringProperty(required=True)
  create_date = db.DateTimeProperty(auto_now_add=True)
  password = db.StringProperty(required=True)
  email = db.EmailProperty(required=True)
  photo_url = db.StringProperty(default=settings.DEFAULT_USER_PHOTO)
  
  status_message = db.StringFlyProperty(default="")
  
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
  
  def put(self, is_guest=False):
    """User could be built from sessions, need write through these users"""
    super(User, self).put()
    
    if is_guest:
      return
      
    from auth import get_current_user, update_current_user
    
    user = get_current_user()
    
    if user and user.username == self.username:
      update_current_user(self)
    
  def can_view(self, user):
    """docstring for can_view"""
    return True
    
  def can_edit(self, user):
    """docstring for can_edit"""
    return self.key() == user.key()
  
  def full_photo(self):
    """docstring for full_photo"""
    return self.photo_url

@cache_result('guest-user-object', 360)
def _get_guest_user():
  """docstring for _get_guest_user"""
  guest = User.all().filter('username', "__GuestUserName").get()
  if not guest:
    guest = User(fullname="Guest", username="__GuestUserName", 
               email="guest@chrisw", password="pwd")
    guest.put(is_guest=True)
  return guest

Guest = _get_guest_user()
