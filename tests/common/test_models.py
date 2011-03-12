#!/usr/bin/env python
# encoding: utf-8
"""
test_models.py

Created by Kang Zhang on 2011-03-11.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

import unittest
from chrisw import db
from common import models as ndb


LOVE = 'love'

class TestHuman(ndb.Entity):
  """docstring for TestHuman"""
  name = db.StringProperty()
  
  def love(self, other):
    """docstring for love"""
    self.create_relation(LOVE, other)
  
  def is_loving(self, other):
    """docstring for is_loving"""
    return self.has_relation(LOVE, other)
  
  def unlove(self, other):
    """docstring for unlove"""
    self.delete_relation(LOVE, other)
  
  def get_lovers(self):
    """docstring for get_lovers"""
    return self.get_target_keys(LOVE, TestHuman)

class TestEntityRelationTestCase(unittest.TestCase):
  """docstring for TestEntityRelationTestCase"""
  def test_love(self):
    """docstring for test_love"""
    lap = TestHuman(name='lap')
    lap.put()
    
    top = TestHuman(name='top')
    top.put()
    
    self.assertFalse(lap.is_loving(top))
    self.assertFalse(top.is_loving(lap))
    
    lap.love(top)
    
    self.assertTrue(lap.is_loving(top))
    self.assertFalse(top.is_loving(lap))
    
    top.love(lap)
    
    self.assertTrue(lap.is_loving(top))
    self.assertTrue(top.is_loving(lap))
    
    lap_lovers = lap.get_lovers()
    self.assertEqual(lap_lovers[0], top.key())
    
    lap.unlove(top)
    
    self.assertEqual(lap.get_lovers(), [])
    self.assertFalse(lap.is_loving(top))
    self.assertTrue(top.is_loving(lap))
    
    top.unlove(lap)
    
    lap.delete()
    top.delete()


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
  def __init__(self, *args, **kwargs):
    """docstring for __init__"""
    kwargs['is_comment'] = True
    super(TestTalkComment, self).__init__(*args, **kwargs)
  
  
  


  
    
    
  
suite = unittest.TestLoader().loadTestsFromTestCase(TestEntityRelationTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)

        

