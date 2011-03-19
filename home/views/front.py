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
  
  topics = GroupTopic.latest().fetch(20)
  streams = UserStream.latest().fetch(20)
  
  recent_members = [x for x in User.latest().fetch(5) if x.key() != Guest.key()]
  
  recent_groups = Group.latest().fetch(5)
  
  return template('home_front_page.html', locals())