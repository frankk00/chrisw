#!/usr/bin/env python
# encoding: utf-8
"""
test_models.py

Created by Kang Zhang on 2011-03-11.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

import unittest
import logging

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
  
  def setUp(self):
    """docstring for setUp"""
    for lap in TestHuman.all():
      lap.delete()
  
  def test_love(self):
    """Test the Entity and Relation API"""
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
    self.assertEqual(list(lap_lovers)[0], top.key())
    
    lap.unlove(top)
    
    self.assertEqual(list(lap.get_lovers()), [])
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
  def get_cls_type_name(cls):
    """docstring for get_cls_type_name"""
    return cls.type_name
  
  type_name = 'TestTalk'

class TestTalkComment(TestTalk):
  """docstring for TestTalkComment"""
  def __init__(self, *args, **kwargs):
    """docstring for __init__"""
    kwargs['is_comment'] = True
    super(TestTalkComment, self).__init__(*args, **kwargs)

class TestMessageIndex(unittest.TestCase):
  """docstring for TestMessageIndex"""
  
  def setUp(self):
    """docstring for setUp"""
    for lap in TestHuman.all():
      lap.delete()
    
    for top in TestTalk.all():
      top.delete()
    
    for foo in TestTalkComment.all():
      foo.delete()
  
  def test_message_index(self):
    """Test for MessageIndex and the Subscriptions"""
    lap = TestHuman(name='lap')
    lap.put()
    
    top = TestHuman(name='top')
    top.put()
    
    lap_post = TestTalk(content='lap post')
    lap_post.put()
    
    self.assertFalse(lap_post.has_subscriber(lap))
    self.assertFalse(lap_post.has_subscriber(top))
    
    lap_post.add_subscriber(lap)
    
    self.assertTrue(lap_post.has_subscriber(lap))
    self.assertFalse(lap_post.has_subscriber(top))
    
    self.assertEqual(list(lap_post.get_subscriber_keys()), [lap.key()])
    
    self.assertNotEqual([lap_post.key()], list(TestTalk.latest_keys_by_subscriber(top))[:1])
    self.assertNotEqual([lap_post.key()], list(TestTalk.latest_keys_by_subscriber(lap))[:1])
    
    lap_post.notify_subscribers()
    
    self.assertEqual([lap_post.key()], list(TestTalk.latest_keys_by_subscriber(lap))[:1])
    self.assertNotEqual([lap_post.key()], list(TestTalk.latest_keys_by_subscriber(top))[:1])
    
    lap_post.add_subscriber(top)
  
    top_post = TestTalkComment(content='top post')
    top_post.put()
    
    top_post.add_subscriber([lap, top])
    
    self.assertNotEqual([top.key()], list(TestTalk.latest_keys_by_subscriber(top))[:1])
    self.assertNotEqual([lap.key()], list(TestTalk.latest_keys_by_subscriber(lap))[:1])
    
    top_post.notify_subscribers()

    self.assertEqual([top_post.key()], list(TestTalkComment.latest_keys_by_subscriber(lap))[:1])
    self.assertEqual([top_post.key()], list(TestTalkComment.latest_keys_by_subscriber(top))[:1])
    
    lap_post.notify_subscribers()
    top_post.delete_subscriber(lap)
    top_post.notify_subscribers()
    
    self.assertEqual([lap_post.key()], list(TestTalkComment.latest_keys_by_subscriber(lap))[:1])
    self.assertEqual([top_post.key()], list(TestTalkComment.latest_keys_by_subscriber(top))[:1])
    
    lap_post.delete()
    top_post.delete()
    
    lap.delete()
    top_post.delete()
    
  

        

