#!/usr/bin/env python
# encoding: utf-8
"""
test_models.py

Created by Kang Zhang on 2011-03-11.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw import db
from common import models as ndb

follow = 'follow'

class TestHuman(ndb.Entity):
  """docstring for TestHuman"""
  name = db.StringProperty()
  
  def follow(self, other):
    """docstring for love"""
    self.get_rel

class TestTalk(ndb.Message):
  """docstring for TestTalk"""
  
  is_comment = db.BooleanProperty(default=False)
  content = db.StringProperty()
  
  @classmethod
  def all(cls, **kwargs):
    """docstring for all"""
    super(TestTalk, cls).all(**kwargs).filter('is_comment', is_comment)
  
  @classmethod
  def get_cls_type_name(self):
    """docstring for get_cls_type_name"""
    return type_name
  
  type_name = 'TestTalk'

class TestTalkComment(TestTalk):
  """docstring for TestTalkComment"""
  is_comment = db.BooleanProperty(default=True)
  


  
    
    
  
    
        

