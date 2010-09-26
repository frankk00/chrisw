#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import views
import settings

from views import create_login_url

apps = [('/index', views.FrontPageHandler),
        ('/signin', views.SignupUserHanlder),
        # since loging url is needed to do authentication
        (settings.LOGIN_URL, views.LoginUserHandler),
        ('/test_login', views.LoginDemoHandler),
        ('/', views.MainHandler)
        ]
