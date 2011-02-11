#!/usr/bin/env python
# encoding: utf-8
"""
appengin_config.py

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import os, sys

from conf import settings

# patch for libs
sys.path += settings.LIB_DIRS

from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key=settings.COOKIE_KEY)
    return app

