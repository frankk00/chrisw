#!/usr/bin/env python
# encoding: utf-8
"""
thingui.py

Created by Kang Zhang on 2011-04-12.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw.core import handlers
from chrisw.core.action import *
from chrisw.core.ui import ModelUI, check_permission
from chrisw.core.memcache import cache_action
from chrisw.i18n import _
from chrisw.helper import Page, djangoforms
from chrisw.helper.django_helper import fields, forms

from common.auth import get_current_user
from group.models import *
from common.models import User
from topic import TopicForm
from conf import settings


class ThingUI(ModelUI):
  """docstring for ThingUI"""

  thing_meta = None

  def __init__(self, thing):
    super(ThingUI, self).__init__(thing)
    self.thing = thing


class ThingHandler(handlers.RequestHandler):
  """Here we use a trick to enable 'mixin' feature for Python.
  Consider the following code example:

  >>> class A():
  ...   def foo(self):
  ...     self.bar()

  >>> class B():
  ...   def bar(self):
  ...     print "bar"

  >>> C = type('C', (A, B, object),{})
  >>> C().foo()
  bar

  """

  thing_meta = None

  def get(self, thing_id):
    """docstring for get"""
    thing = thing_meta.thing_class.get_by_id(thing_id)
    thing_ui = thing_meta.thing_ui_class(thing)

    self.get_impl(thing_ui)

  def post(self, thing_id):
    """docstring for post"""
    thing = thing_meta.thing_class.get_by_id(thing_id)
    thing_ui = thing_meta.thing_ui_class(thing)

    self.post_impl(thing_ui, self.request)


