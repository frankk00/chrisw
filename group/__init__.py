#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Kang Zhang on 2010-09-25.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import views
import settings

apps = [(r'/group/(\d+)', views.GroupHandler),
        (r'/group/new', views.NewGroupHandler),
        (r'/group/topic/(\d+)', views.TopicHandler),
        (r'/group/topic/new', views.NewTopicHandler),
        ]