#!/usr/bin/env python
# encoding: utf-8
"""
stream_render.py

Created by Kang Zhang on 2011-03-19.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from django import template

from chrisw.i18n import _
from chrisw.helper.django_helper import render_to_string

from home.models import TEXT_STREAM

register = template.Library()

class UserStreamRenderNode(template.Node):
  """docstring for StreamRenderNode"""
  def __init__(self, stream_name, display_name=False):
    super(UserStreamRenderNode, self).__init__()
    self.stream_name = stream_name
    self.display_name = display_name
  
  def render(self, context):
    """docstring for render"""
    
    stream = context[self.stream_name]
    display_name = self.display_name
    
    context.update(locals())
    
    if not stream:
      return "Skipped"
    
    if stream.target_type == TEXT_STREAM or stream.target_type is None:
      return render_to_string("item_text_user_stream.html", context)
    
    raise Exception("Can't render this type of stream %s %s" % \
      (stream, stream.target_type))

@register.tag
def stream_render(parser, token):
  items = token.split_contents()
  
  if len(items) < 2:
    raise template.TemplateSyntaxError("%r tag takes at least 2 arguments" % \
      items[0])
  
  stream_name = items[1]
  args = {}
  
  for item in items[2:]:
    if item == "with_name":
      args["display_name"] = True
    else:
      raise template.TemplateSyntaxError("%r tag got an unknown argument: %r"\
        % (items[0], item))
  
  return UserStreamRenderNode(stream_name, **args)
