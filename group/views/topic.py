#!/usr/bin/env python
# encoding: utf-8
"""
topic.py

Notice this file is the demostration for the new style handler. Don't change
it to class handler style that in other files.

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""


import logging

from chrisw.core.action import *
from chrisw.core.ui import ModelUI, check_permission
from chrisw.i18n import _
from chrisw.helper import Page, djangoforms
from chrisw.helper.django_helper import fields, forms
from chrisw.web.util import *

from common.auth import get_current_user
from conf import settings
from group.models import *


class TopicForm(djangoforms.ModelForm):
  """docstring for TopicForm"""
  class Meta:
    model = GroupTopic
    fields = ['title', 'content']
  
  title = fields.CharField(label = _('Topic Title'), min_length=2,\
    max_length=30)
  content = fields.CharField(label = _('Topic Content'), min_length=5,\
    widget=forms.Textarea, max_length=5000)

class PostForm(djangoforms.ModelForm):
  """docstring for PostForm"""
  class Meta:
    model = GroupPost
    fields = ['content']
  
  content = fields.CharField(label = _('Post Content'), min_length=1,\
    widget=forms.Textarea, max_length=2000)

class TopicUI(ModelUI):
  """docstring for TopicUI"""
  def __init__(self, topic):
    super(TopicUI, self).__init__(topic)
    self.topic = topic
    self.current_user = get_current_user()
  
  #allow guest usesrs to login
  #@check_permission('view', "Not allowed to open topic")
  def view(self, request):
    """docstring for view"""
    limit = int(request.get('limit', '20'))
    offset = int(request.get('offset', '0'))
  
    query = self.topic.get_all_posts(has_order=True)
    post_form = PostForm()
    page = Page(query=query, offset=offset, limit=limit, request=request)
    posts = page.data()
    
    self.topic.hits += 1
    self.topic.put()
    
    return template('topic_display', locals())
  
  @check_permission('edit', "Not the author")
  def edit(self):
    """docstring for edit"""
    form = TopicForm(data=self.topic.to_dict())
    post_url = '/group/topic/%d/edit' % self.topic.key().id()
    return template('item_new', locals())
  
  @check_permission('edit', "Not the author")
  def edit_post(self, request):
    """docstring for edit_post"""
    form = GroupTopic(data=request.POST, instance=self.topic)
    if form.is_valid():
      new_topic = form.save(commit=False)
      new_topic.put()
      return redirect('/group/topic/%d' % new_topic.key().id())
    return template('item_new', locals())
  
  @check_permission('delete', "Can't delete topic")
  def delete(self):
    """docstring for delete"""
    pass
  
  @check_permission('create_post', "Not allowed to reply the thread")
  def create_post(self):
    """docstring for create_post"""
    form = PostForm()
    post_url = '/group/topic/%d/new' % self.topic.key().id()
    return template('item_new', locals())
  
  @check_permission('create_post', "Not allowed to reply the thread")
  def create_post_post(self, request):
    """docstring for create_post_post"""
    form = PostForm(data=request.POST)
    if form.is_valid():
      
      new_post = form.save(commit=False)
      self.topic.create_post(new_post, self.current_user)
      
      return redirect('/group/topic/%d' % self.topic.key().id())
    return template('item_new', locals())

def topic_handler(func):
  """docstring for topic_handler"""
  def wrapper(handler, topic_id):
    """docstring for wrapper"""
    topic = GroupTopic.get_by_id(int(topic_id))
    topic_ui = TopicUI(topic)
    
    return func(topic_ui, handler.request)
    
  return wrapper

@get_handler(r'/group/topic/(\d+)')
@topic_handler
def topic_view_get(topic_ui, request):
  """docstring for topic_view_handler"""
  return topic_ui.view(request)

@get_handler(r'/group/topic/(\d+)/new')
@topic_handler
def topic_create_post_get(topic_ui, request):
  """docstring for topic_new_get"""
  return topic_ui.create_post()
  
@post_handler(r'/group/topic/(\d+)/new')
@topic_handler
def topic_create_post_post(topic_ui, request):
  """docstring for topic_new_post"""
  return topic_ui.create_post_post(request)

@get_handler(r'/group/topic/(\d+)/edit')
@topic_handler
def topic_edit_get(topic_ui, request):
  """docstring for topic_edit_get"""
  return topic_ui.edit()

@post_handler(r'/group/topic/(\d+)/edit')
@topic_handler
def topic_edit_post(topic_ui, request):
  """docstring for topic_edit_post"""
  return topic_ui.edit_post(request)
