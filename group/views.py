import logging
import settings

from google.appengine.ext import webapp
from google.appengine.ext.db import djangoforms

from duser.auth import login_required, get_current_user
from api.webapp import api_enabled

from models import *

class GroupHandler(webapp.RequestHandler):
  """docstring for GroupHandler"""
  
  @login_required
  @api_enabled
  def get(self, group_id):
    """docstring for get"""
    group = Group.get_by_id(int(group_id))
    return 'group_display.html', locals()

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

    


