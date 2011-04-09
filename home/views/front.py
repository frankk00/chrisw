#!/usr/bin/env python
# encoding: utf-8
"""
front.py

Created by Kang Zhang on 2011-03-19.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

from chrisw.core.action import *
from chrisw.core.ui import ModelUI, check_permission
from chrisw.core.memcache import cache_action
from chrisw.i18n import _
from chrisw.helper import Page, djangoforms
from chrisw.helper.django_helper import fields, forms
from chrisw.web.util import *

from common.auth import get_current_user, Guest
from conf import settings
from group.models import *
from home.models import *

@get_handler(r'/home')
def display_home_page(request):
  """docstring for topic_edit_post"""
  
  topics = GroupTopic.latest().fetch(12)
  streams = UserStream.latest().fetch(12)
  
  recent_members = [x for x in User.latest().fetch(5) if x.key() != Guest.key()]
  
  recent_groups = Group.latest().fetch(5)
  
  display_group_name = True
  
  return template('page_site_home_v1.html', locals())