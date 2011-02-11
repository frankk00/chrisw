#!/usr/bin/env python
# encoding: utf-8
"""
group.py

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

from google.appengine.ext import webapp, db
from google.appengine.ext.db import djangoforms

from duser.auth import get_current_user
from api.webapp import *
from group.models import *
from duser.models import User
from topic import TopicForm
from api.helpers import fields, forms
from conf import settings

from api.i18n import _

class GroupForm(djangoforms.ModelForm):
  class Meta:
    model = Group
    fields = ['title', 'introduction']
  
  title = fields.CharField(label = _("Group Title"), min_length=2,\
    max_length=10)
  introduction = fields.CharField(label = _("Group Introductioin"),\
    widget=forms.Textarea, min_length=2, max_length = 2000)

class GroupPhotoForm(forms.Form):
  """docstring for ProfilePhoto"""
  photo = fields.ImageField(label = _("Group Picture"))

class GroupUI(PermissionUI):
  """docstring for GroupUI"""
  def __init__(self, group):
    super(GroupUI, self).__init__(group)
    self.group = group
  
  @view_method
  # it dosen't need check permission, as it's opened to all people. include th
  # the guest account
  # @check_permission('view', "Not allowed to open the group")
  def view(self, request):
    """docstring for view"""
    limit = int(request.get('limit', '20'))
    offset = int(request.get('offset', '0'))
    query = self.group.get_topics()
    count = query.count(2000)
    topics = query.fetch(limit, offset)
    
    members = [User.get_by_id(mk) for mk in self.group.member_ids]
    
    var_dict = locals() # can't assign variable below this line
    
    from api.helpers import inspect_permissions
    var_dict.update( inspect_permissions(self.group, get_current_user()) )
            
    return template('group_display.html', var_dict)
  
  @view_method
  @check_permission('edit', "Not a admin user")
  def edit(self, request):
    """docstring for edit"""
    
    if request.get('image_url', ''):
      self.group.photo_url = request.get('image_url')
      self.group.put()
    
    form = GroupForm(data=self.group.to_dict())
    post_url = '/group/%d/edit' % self.group.key().id()
    
    from front.views import photo
    photo_form = GroupPhotoForm()
    photo_upload_url = photo.create_upload_url()
    back_url = request.path
    
    return template('group_settings', locals())
  
  @check_permission('edit', "Not a admin user")
  def edit_post(self, request):
    """the post_back handler for edit group info"""
    form = GroupForm(data=request.POST, instance=self.group)
    if form.is_valid():
      new_group = form.save(commit=False)
      new_group.put()
      return redirect('/group/%d' % self.group.key().id())
    return template('item_new', locals())
    
  """ deprecated  
  @view_method
  @check_permission('view', "Not allowed to open the group")
  def query(self, request):
    ""docstring for query""
    return self.query_post(request)
  
  @check_permission('view', "Not allowed to open the group")
  def query_post(self, request):
    ""Return the topic contains in this group, ordered by time
    ""
    
    limit = int(request.get('limit', '20'))
    offset = int(request.get('offset', '0'))
    
    topics = self.group.get_topics().fetch(limit, offset)
    items = topics
    return template('item_list', locals())
  """  
  
  @view_method
  @check_permission('join', "Can't join group")
  def join(self):
    """docstring for join"""
    self.group.join(get_current_user())
    return back()
  
  @view_method
  @check_permission('delete', "Cant' delete topic")
  def delete(self):
    """docstring for delete"""
    message = 'Topic has been successfully deleted.'
    self.group.delete()
    return back()
  
  @view_method
  @check_permission('quit', "Is not member")
  def quit(self):
    """docstring for quite"""
    pass
  
  @view_method
  @check_permission('create_topic', "Not allowed to create topic here")
  def create_topic(self):
    """docstring for create_topic"""
    form = TopicForm()
    post_url = '/group/%d/new' % self.group.key().id()
    return template('item_new', locals())
    
  @check_permission('create_topic', "Not allowed to create topic here")
  def create_topic_post(self, request):
    """docstring for create_topic_post"""
    form = TopicForm(data=request.POST)
    if form.is_valid():
      new_topic = form.save(commit=False)
      new_topic.group = self.group
      new_topic.author = get_current_user()
      new_topic.put()
      return redirect('/group/topic/%d' % new_topic.key().id())
    return template('item_new', locals())

class GroupHandler(webapp.RequestHandler):
  """docstring for GroupHandler"""
  def get_impl(self, groupui):
    """docstring for get_impl"""
    raise Exception("Have not implemented")
  
  def post_impl(self, groupui, request):
    """docstring for post_impl"""
    return self.get_impl(groupui)

  @api_enabled
  def get(self, group_id):
    """docstring for get"""
    group = Group.get_by_id(int(group_id))
    return self.get_impl(GroupUI(group))
  
  @api_enabled
  def post(self, group_id):
    """docstring for post"""
    group = Group.get_by_id(int(group_id))
    return self.post_impl(GroupUI(group), self.request)

class GroupViewHandler(GroupHandler):
  """docstring for GroupViewHandler"""
  def get_impl(self, groupui):
    """docstring for get_impl"""
    return groupui.view(self.request)

class GroupNewTopicHandler(GroupHandler):
  """docstring for GroupNewTopicHandler"""
  def get_impl(self, groupui):
    return groupui.create_topic()
  
  def post_impl(self, groupui, request):
    return groupui.create_topic_post(request)

class GroupEditHandler(GroupHandler):
  """docstring for GroupNewTopicHandler"""
  def get_impl(self, groupui):
    return groupui.edit(self.request)
    
  def post_impl(self, groupui, request):
    return groupui.edit_post(request)

"""
class GroupQueryHandler(GroupHandler):
  def get_impl(self, groupui):
    return groupui.query(self.request)

  def post_impl(self, groupui, request):
    return groupui.query_post(request)
"""
class GroupJoinHandler(GroupHandler):
  """docstring for GroupNewTopicHandler"""
  def get_impl(self, groupui):
    return groupui.join()

class GroupQuitHandler(GroupHandler):
  """docstring for GroupQuitHandler"""
  def get_impl(self, groupui):
    """docstring for get_impl"""
    return groupui.quit()
    

class GroupDeleteHandler(GroupHandler):
  """docstring for GroupDeleteHandler"""
  def get_impl(self, groupui):
    groupui.delete()
    

apps = [(r'/group/(\d+)', GroupViewHandler),
        #(r'/group/(\d+)/query', GroupQueryHandler),
        (r'/group/(\d+)/new', GroupNewTopicHandler),
        (r'/group/(\d+)/join', GroupJoinHandler),
        (r'/group/(\d+)/edit', GroupEditHandler),
        (r'/group/(\d+)/delete', GroupDeleteHandler),
        (r'/group/(\d+)/quit', GroupQuitHandler),
        ]
