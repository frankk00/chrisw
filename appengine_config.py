#!/usr/bin/env python
# encoding: utf-8
"""
appengin_config.py

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import os, sys
import settings

# patch for libs
sys.path += settings.LIB_DIRS

# need be regenerated before production release, for security reasons :-)
#COOKIE_KEY = os.urandom(64)
COOKIE_KEY = '\xe4\xc0z\xc0|\x0b*o\xe7<\xe4i?\xf3X\x04\xc6\xad\x92\x87\x9d\xc3|\xdcj\x9b\x80S\xf6\x11\xc7\xaef\xfa\x89\xa2\xe9\xe4\x87\xb9rm\x1bk\x8f\xdf\xf9\xff\xca\xb4M-\xfc))\xdd\xa8\xe2\x9e\xdc%\x1dy0'

from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
    return app

