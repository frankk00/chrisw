#!/usr/bin/env python
# encoding: utf-8
"""
settings.py

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import os

from local_settings import *

APP_ID = "daoshicha"

# django template path config

ROOT_PATH = os.path.dirname(__file__)

TEMPLATE_DIRS = (ROOT_PATH + "/templates",
                 ROOT_PATH + "/front/templates",
                 ROOT_PATH + "/group/templates",
                )

LIB_DIRS = (ROOT_PATH + "/lib",)

LOGIN_URL = "/login"

DEFAULT_HOME = "/group"

INSTALLED_APPS = ('front')

DEFAULT_USER_PHOTO = "http://www.waynejohn.com/wp-content/uploads/WindowsLiveWriter/WayneSimpson_120F1/_1221625200_102_thumb.gif"

DEFAULT_GROUP_PHOTO = DEFAULT_USER_PHOTO

