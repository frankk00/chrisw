import logging
import settings

from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms

from duser.auth import get_current_user
from api.webapp import login_required, api_enabled
from api.webapp import check_permission, view_method, PermissionUI

from models import *

class GroupUI(PermissionUI):
  """docstring for GroupUI"""
  def __init__(self, group):
    super(GroupUI, self).__init__(group)
    self.group = group
  
  @view_method
  @check_permission('view', "Not allowed to open the group")
  def view(self):
    """docstring for view"""
    return 'group_display.html', locals()
  
  @view_method
  @check_permission('edit', "Not a admin user")
  def edit(self):
    """docstring for edit"""
    pass
  
  @check_permission('edit', "Not a admin user")
  def edit_post(self, request):
    """the post_back handler for edit group info"""
    pass
  
  @view_method
  @check_permission('create_thread', "Not allowed to create thread here")
  def create_thread(self):
    """docstring for create_thread"""
    pass
    
  @check_permission('create_thread', "Not allowed to create thread here")
  def create_thread_post(self):
    """docstring for create_thread_post"""
    pass

class GroupHandler(webapp.RequestHandler):
  """docstring for GroupHandler"""
  
  @api_enabled
  def get(self, group_id):
    """docstring for get"""
    group = Group.get_by_id(int(group_id))
    return GroupUI(group).view()

class TopicHandler(webapp.RequestHandler):
  """docstring for TopicHandler"""
  @login_required
  @api_enabled
  def get(self, topic_id):
    """docstring for get"""
    topic = Topic.get_by_id(int(topic_id))
    return 'topic_display.html', locals()
    
class NewItemHandler(webapp.RequestHandler):
  """docstring for NewItemHandler"""
  
  def create_form(self, *args):
    """docstring for create_item"""
    raise Exception("Has not been implementation")
    
  def template_name(self):
    """docstring for template_name"""
    raise Exception("Has not been implementation")
  
  @login_required
  @api_enabled
  def get(self):
    """docstring for get"""
    form = self.create_form()
    return self.template_name(), locals()
  
  @login_required
  @api_enabled
  def post(self):
    """docstring for post"""
    form = self.create_form(data = self.request.POST)
    if form.is_valid():
      logging.debug("want to save group")
      group = form.save(commit=False)
      group.create_user = get_current_user()
      group.put()
    
    return self.template_name(), locals()

class GroupForm(djangoforms.ModelForm):
  class Meta:
    model = Group
    fields = ['title', 'introduction']

class NewGroupHandler(NewItemHandler):
  """docstring for CreateGroupHandler"""
  
  def create_form(self, *args):
    return GroupForm(*args)
    
  def template_name(self):
    return 'item_new.html'

class NewTopicHandler(NewItemHandler):
  def create_form(self, *args):
    """docstring for create_form"""
    return TopicForm(*args)
  
  def template_name(self):
    """docstring for template_name"""
    return 'item_new.html'

class TopicForm(djangoforms.ModelForm):
  """docstring for TopicForm"""
  class Meta:
    model = Topic

    


