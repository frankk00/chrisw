#!/usr/bin/env python
# encoding: utf-8
"""
auth.py

The authentication libs

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging
import chrisw.auth

from models import *
from chrisw.auth import login, logout, update_current_user


def authenticate(username='', password=''):
  """Return a user object"""
  user = User.all().filter("username =", username.strip()) \
                   .filter("password =", password.strip()).get()
  return user

def get_current_user():
  """docstring for get_current_user"""
  return chrisw.auth.get_current_user(Guest)





