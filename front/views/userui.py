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

# import form fields
try:
  # for django 1.1
  from django.forms import CharField
  from django import forms as fields
except ImportError:
  # django 0.9
  from django.db import models as fields

from duser.auth import get_current_user

from duser import auth
from api.webapp import login_required, api_enabled, template, redirect
from api.shortcuts import render_to_string



