#!/usr/bin/env python
# encoding: utf-8
"""
topic.py

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""


import logging

from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms

from duser.auth import get_current_user
from api.webapp import login_required, api_enabled
from api.webapp import check_permission, view_method, PermissionUI
from api.webapp import template, redirect
from api.i18n import _

from conf import settings
from group.models import *

from api.helpers import fields, forms, Page

class TopicForm(djangoforms.ModelForm):
  """docstring for TopicForm"""
  class Meta:
    model = Topic
    fields = ['title', 'content']
  
  title = fields.CharField(label = _('Topic Title'), min_length=2,\
    max_length=30)
  content = fields.CharField(label = _('Topic Content'), min_length=5,\
    widget=forms.Textarea, max_length=5000)

class PostForm(djangoforms.ModelForm):
  """docstring for PostForm"""
  class Meta:
    model = Post
    fields = ['content']
  
  content = fields.CharField(label = _('Post Content'), min_length=1,\
    widget=forms.Textarea, max_length=2000)

class TopicUI(PermissionUI):
  """docstring for TopicUI"""
  def __init__(self, topic):
    super(TopicUI, self).__init__(topic)
    self.topic = topic
  
  @view_method
  #allow guest usesrs to login
  #@check_permission('view', "Not allowed to open topic")
  def view(self, request):
    """docstring for view"""
    limit = int(request.get('limit', '20'))
    offset = int(request.get('offset', '0'))
    query = self.topic.get_posts()
    count = query.count(2000)
    posts = query.fetch(limit, offset)
    post_form = PostForm()
    page = Page(count=count, offset=offset, limit=limit, request=request)
    
    self.topic.hits += 1
    self.topic.put()
    
    return template('topic_display', locals())
  
  @view_method
  @check_permission('edit', "Not the author")
  def edit(self):
    """docstring for edit"""
    form = TopicForm(data=self.topic.to_dict())
    post_url = '/group/topic/%d/edit' % self.topic.key().id()
    return template('item_new', locals())
  
  @view_method
  @check_permission('edit', "Not the author")
  def edit_post(self, request):
    """docstring for edit_post"""
    form = Topic(data=request.POST, instance=self.topic)
    if form.is_valid():
      new_topic = form.save(commit=False)
      new_topic.put()
      return redirect('/group/topic/%d' % new_topic.key().id())
    return template('item_new', locals())
  
  @view_method
  @check_permission('delete', "Can't delete topic")
  def delete(self):
    """docstring for delete"""
    pass
  
  @view_method
  @check_permission('reply', "Not allowed to reply the thread")
  def create_post(self):
    """docstring for create_post"""
    form = PostForm()
    post_url = '/group/topic/%d/new' % self.topic.key().id()
    return template('item_new', locals())
  
  @view_method
  @check_permission('reply', "Not allowed to reply the thread")
  def create_post_post(self, request):
    """docstring for create_post_post"""
    form = PostForm(data=request.POST)
    if form.is_valid():
      logging.debug("created a new post ")
      new_post = form.save(commit=False)
      new_post.topic = self.topic
      new_post.author = get_current_user()
      new_post.put()
      
      # update the topic's update time
      import datetime
      self.topic.update_time = datetime.datetime.now()
      self.topic.length += 1
      self.topic.put()
      
      return redirect('/group/topic/%d' % self.topic.key().id())
    return template('item_new', locals())


class TopicHandler(webapp.RequestHandler):
  """docstring for GroupHandler"""
  def get_impl(self, topic):
    """docstring for get_impl"""
    raise Exception("Have not implemented")

  def post_impl(self, topic, request):
    """docstring for post_impl"""
    return self.get_impl(topic)

  @api_enabled
  def get(self, topic_id):
    """docstring for get"""
    topic = Topic.get_by_id(int(topic_id))
    return self.get_impl(TopicUI(topic))

  @api_enabled
  def post(self, topic_id):
    """docstring for post"""
    topic = Topic.get_by_id(int(topic_id))
    return self.post_impl(TopicUI(topic), self.request)

class TopicViewHandler(TopicHandler):
  """docstring for GroupViewHandler"""
  def get_impl(self, topic):
    """docstring for get_impl"""
    return topic.view(self.request)

class TopicNewPostHandler(TopicHandler):
  """docstring for GroupNewTopicHandler"""
  def get_impl(self, topic):
    return topic.create_post()

  def post_impl(self, topic, request):
    return topic.create_post_post(request)

class TopicEditHandler(TopicHandler):
  """docstring for GroupNewTopicHandler"""
  def get_impl(self, topic):
    return topic.edit()

  def post_impl(self, topic, request):
    return topic.edit_post(request)


apps = [(r'/group/topic/(\d+)', TopicViewHandler),
        (r'/group/topic/(\d+)/new', TopicNewPostHandler),
        (r'/group/topic/(\d+)/edit', TopicEditHandler),
        ]
