#!/usr/bin/env python
# encoding: utf-8
"""
db.py

Created by Kang Zhang on 2011-02-18.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

import logging
import datetime
import time

try:
  import cPickle as pickle
except ImportError:
  import pickle

from google.appengine.ext import db
from google.appengine.ext.db import *
from google.appengine.api import datastore_errors
from google.appengine.api.datastore_types import Blob
from google.appengine.ext.db import djangoforms
from django import forms


class DictProperty(db.Property):
  """ 
  """
  def validate(self, value):
    value = super(DictProperty, self).validate(value)
    if not isinstance(value, dict):
      raise Exception("NOT A DICT %s" % value)
    return value

  def default_value(self):
    return {}

  def datastore_type(self):
    return Blob

  def get_value_for_datastore(self, model_instance):
    value = super(DictProperty, self).get_value_for_datastore(model_instance)
    return Blob(pickle.dumps(value, protocol=-1))

  def make_value_from_datastore(self, model_instance):
    value = super(DictProperty, self).make_value_from_datastore(model_instance)
    return pickle.loads(str(value))

class WeakReferenceProperty(db.Property):
  """WeakReference is designed to store only the Key for the model"""
  def validate(self, value):
    """docstring for validate"""
    value = super(WeakReferenceProperty, self).validate(value)
    
    if isinstance(value, Model):
      value = value.key()
      
    if not isinstance(value, Key):
      raise Exception("Not a Key %s" % value)
    return value
  
  def get_value_for_datastore(self, model_instance):
    """docstring for get_value_for_datastore"""
    value = super(WeakReferenceProperty, self).get_value_for_datastore(model_instance)
    return str(value)
  
  def make_value_from_datastore(self, model_instance):
    """docstring for make_value_from_datastore"""
    value = super(WeakReferenceProperty, self).make_value_from_datastore(model_instance)
    return Key(value)

class FlyProperty(object):
  """FlyProperty is something lightweight than normal property and it cannot 
  be in search field
  """
  
  def __init__(self, default=None, name = None):
    """docstring for __init__"""
    self.default = None
    self.name = name
  
  def __property_config__(self, model_class, property_name, dct):
    """docstring for __property_config"""
    if not dct.has_key('extra_dict'):
      raise Exception('Model %s is not a subclass of FatModel' % \
                        type(owner_cls))
                        
    self.model_class = model_class
    if self.name is None:
      self.name = property_name
    
  def __get__(self, owner_instance, owner_cls):
    """docstring for __get__"""
    
    if owner_instance:
      return owner_instance.extra_dict.get(self.name, self.default)
    else:
      return self;
  
  def __set__(self, owner_instance, value):
    """docstring for __set__"""
    owner_instance.extra_dict.set(self.name, value)

SIMPLE_TYPES = (int, long, float, bool, dict, basestring)

def to_dict(model):
  output = {}
  
  if isinstance(model, db.Model):
    # model is db.Model
    items = model.properties().iteritems()
    output['model_class'] = model.__class__.__name__
    
    try:
      output['model_id'] = model.key().id()
    except db.NotSavedError, e:
      output['model_id'] = "undefined"
  elif isinstance(model, db.Key):
    return to_dict(db.get(model))
  elif hasattr(model, 'items'):
    items = model.items()
  elif isinstance(model, SIMPLE_TYPES) or model is None:
    return model
  else:
    logging.debug("Can't to dict item %s", model.__dict__)
    # temprary fix, need be recheck again, it's caused by django's 
    return str(model._proxy____args)
    
  if hasattr(model, 'can_visit_key'):
    check_key = model.can_visit_key
  else:
    check_key = lambda x, y : True # can be visited by default
  
  from duser import auth
  user = auth.get_current_user()
  
  for key, prop in items:
    
    if not check_key(user, key):
      # can't be visited since privacy control
      continue
      
    try:
      value = getattr(model, key)
    except datastore_errors.Error:
      value = None
    except AttributeError:
      value = prop
    
    if value is None or isinstance(value, SIMPLE_TYPES):
      output[key] = value
    elif isinstance(value, datetime.date):
      # Convert date/datetime to ms-since-epoch ("new Date()").
      logging.debug(" datetime: %s", value)
      ms = time.mktime(value.utctimetuple()) * 1000
      ms += getattr(value, 'microseconds', 0) / 1000
      output[key] = int(ms)
    elif isinstance(value, db.Model):
      output[key] = to_dict(value)
    elif isinstance(value, db.Key):
      output[key] = to_dict(db.get(value))
    elif isinstance(value, list):
      output[key] = [ to_dict(x) for x in value]
    elif isinstance(value, djangoforms.ModelForm) or \
         isinstance(value, forms.Form):
      output[key] = {'data': to_dict(value.data),
                     'errors': to_dict(value.errors)}
    else:
      logging.debug('Error from chris.db: cannot encode ' + repr(prop))
      continue
  
  return output
    
class Model(db.Model):
  """docstring for Model"""
  deleted = db.BooleanProperty(default=False)
  
  def to_dict(self):
    return to_dict(self)
  
  def delete(self, **kwargs):
    """docstring for def delete(self, **kwargs):"""
    self.delete = True
    self.put()
  
  @classmethod
  def get(cls, keys, **kwargs):
    """Notice that this method overrides get_by_id and get_by_key_name
    """
    results = super(Model, cls).get(keys)

    if results is None:
      return None

    if isinstance(results, Model):
      instances = [results]
    else:
      instances = results
    
    # filter the deleted result
    instances = [ i for i in instances if not i.deleted]
    
    if instances == []:
      return None
    elif len(instances) == 1:
      return instances[0]
    return instances
  
  @classmethod
  def all(cls, **kwargs):
    """Deleted items has been filtered.
    """
    return super(Model, cls).all(**kwargs).filter('deleted = ', False)
  
  @classmethod
  def gql(cls, query_string, *args, **kwds):
    """
    """
    raise Exception("GQL is not allowed in this extension")

def _initialize_fly_properties(model_class, name, bases, dct):
  """docstring for _initialize_fly_properties"""
  defined = set()
  for attr, prop in dct.items():
    if isinstance(prop, FlyProperty):
      if attr in defined:
        raise Exception("Duplicated FlyProperty %s Dectected", attr)
      defined.add(attr)
      model_class._properties[attr] = prop
      prop.__property_config__(model_class, attr, dct)
  
class FlyPropertiedMeta(type):
  """docstring for FlyPropertiedClass"""
  def __init__(cls, name, bases, dct):
    super(FlyPropertiedMeta, cls).__init__(name, bases, dct)
    
    _initialize_fly_properties(cls, name, bases, dct)
    

class FlyModel(Model):
  """Fot Model added extra_dict on Model to enable the usage of FlyProperty"""
  
  __metaclass__ = FlyPropertiedMeta
  
  extra_dict = DictProperty(default={})
    