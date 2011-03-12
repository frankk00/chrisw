#!/usr/bin/env python
# encoding: utf-8
"""
test_db.py

Created by Kang Zhang on 2011-03-11.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


import unittest
import logging
from chrisw import db

class TestStudent(db.FlyModel):
  """docstring for Student"""
  name = db.StringProperty()
  age = db.FlyProperty()
  sex = db.FlyProperty()

class TestLaptop(db.Model):
  """docstring for Laptop"""
  student = db.WeakReferenceProperty()
    
class DBTestCase(unittest.TestCase):
  """docstring for DBTestCase"""

  
  def create_foo(self):
    """docstring for create_foo"""
    foo = TestStudent()
    foo.name = 'foo'
    foo.age = 1
    foo.sex = 'male'
    foo.put()
    return foo
  
  def query_foo(self):
    """docstring for query_foo"""
    return TestStudent.all().filter('name =', 'foo').get()

  def test_fly_property(self):
    """Test the FlyProperty"""
    foo = self.create_foo()
    
    bar = TestStudent()
    bar.name = 'bar'
    bar.age = 2
    bar.sex = 'female'
    
    
    foo_ref = self.query_foo()
    self.assertEqual(foo_ref.name, 'foo')
    self.assertEqual(foo_ref.age, 1)
    self.assertEqual(foo_ref.sex, 'male')
    
    foo.delete()
  
  def test_weak_reference(self):
    """Test the WeakReferenceProperty"""
    foo = self.create_foo()
    
    lap = TestLaptop()
    lap.student = foo
    lap.put()
    
    top = TestLaptop()
    top.student = foo.key()
    top.put()
    
    lap_ref = TestLaptop.all().filter("student =", foo).get()
    self.assertEqual(lap_ref.student, foo.key())
    
    top_ref = TestLaptop.all().filter("student =", foo.key()).get()
    self.assertEqual(top_ref.student, foo.key())
    
suite = unittest.TestLoader().loadTestsFromTestCase(DBTestCase)
