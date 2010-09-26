#!/usr/bin/env python
# encoding: utf-8
"""
settings.py

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import os

APP_ID = "daoshicha"

# django template path config

ROOT_PATH = os.path.dirname(__file__)

TEMPLATE_DIRS = (ROOT_PATH + "/templates",
                 ROOT_PATH + "/front/templates",
                 ROOT_PATH + "/group/templates",
                )

LIB_DIRS = (ROOT_PATH + "/lib",)

LOGIN_URL = "/login"

