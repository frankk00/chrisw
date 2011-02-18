#!/usr/bin/env python
# encoding: utf-8
"""
settings.py

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import os

from local_settings import *
from chrisw.i18n import _

APP_ID = "daoshicha"

# django template path config

ROOT_PATH, CONFIG_PATH = os.path.split(os.path.dirname(__file__))

TEMPLATE_DIRS = (ROOT_PATH + "/templates",
                 ROOT_PATH + "/front/templates",
                 ROOT_PATH + "/group/templates",
                )

LIB_DIRS = (ROOT_PATH + "/lib",)

LOCALE_PATHS = (ROOT_PATH + '/conf/locale',)

LOGIN_URL = "/login"

DEFAULT_HOME = "/group"

INSTALLED_APPS = ('front',)

DEFAULT_USER_PHOTO = "http://www.gravatar.com/avatar.php?"

DEFAULT_GROUP_PHOTO = "http://www.gravatar.com/avatar/cf4773410a19cd50fc2b8bcaaef9a9dc?s=48"

USE_I18N = True

GRAVATAR_BASE = "http://www.gravatar.com/avatar/"

# Valid languages
LANGUAGES = (
    # 'en', 'zh_TW' match the directories in conf/locale/*
    ('en', 'English'),
    ('zh_CN', 'Chinese'),
    # or ('zh-tw', _('Chinese')), # But the directory must still be conf/locale/zh_TW
    )




