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


SIMPLE_TYPES = (int, long, float, bool, dict, basestring)

def _check_dict_content(dct):
  valid = True
  
  for value in dct.values():
    if value is not None and not isinstance(value, SIMPLE_TYPES + (Key,list)):
      valid = False
    elif isinstance(value, dict):
      valid = _check_dict_content(value) is not None
  
  if valid:
    return dct
  else:
    return None

class DictProperty(db.Property):
  """A property that can be used to store the dict in python. Only simple types
  are allowed in it.
  
  simple types: (int, long, float, bool, dict, basestring), list and db.Key
  """
  def validate(self, value):
    value = super(DictProperty, self).validate(value)
    if not isinstance(value, dict):
      raise Exception("NOT A DICT %s" % value)
    return _check_dict_content(value)

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
    value = super(WeakReferenceProperty, self).validate(value)
    
    if isinstance(value, Model):
      value = value.key()
      
    if not isinstance(value, Key):
      raise Exception("Not a Key %s" % value)
    return value
  
  def default_value(self):
    return Key()
  

class FlyProperty(object):
  """FlyProperty is something lightweight than normal property and it cannot 
  be in search field.
  
  It require the object contan's a DictProperty called extra_dict.
  """
  
  def __init__(self, default=None, name=None, required=False):
    """docstring for __init__"""
    self.default = default
    self.name = name
    self.required = required
  
  def __property_config__(self, model_class, property_name, dct):
    """docstring for __property_config"""
    if not isinstance(model_class, FlyPropertiedMeta):
      raise Exception('Model %s is not a subclass of FatModel' % \
                        type(model_class))
                        
    self.model_class = model_class
    if self.name is None:
      self.name = property_name
  
  def empty(self, value):
    return value is None
  
  def _check_type(self, value):
    """docstring for _type_check"""
    if not isinstance(self.datatype(), list) and \
      isinstance(value, self.datatype()):
      return value
    if any([isinstance(value, t) for t in self.datatype()]):
      return value
      
    raise Exception('Type %s Required, but %s detected', self.datatype(),\
                      value)
  
  def validate(self, value):
    
    if self.required and self.empty(value):
      raise Exception('Property %s is required', self.name)
    
    if value is not None:
      return self._check_type(value)
      
    return value
    
  def __get__(self, owner_instance, owner_cls):
    """Populate the property from dict when it is used."""
    
    if owner_instance:
      value = owner_instance.extra_dict.get(self.name, self.default)
      return value
    else:
      return self;
  
  def __set__(self, owner_instance, value):
    """Write the modification to the extra dict"""
    value = self.validate(value)
    owner_instance.extra_dict[self.name] = value
  
  def datatype(self):
    """docstring for datatype"""
    return self.data_type
  
  data_type = str

class StringFlyProperty(FlyProperty):
  """A string property which will be stored in ``extra_dict``"""
  data_type = basestring

class IntegerFlyProperty(FlyProperty):
  """A integer property which will be stored in ``extra_dict``"""
  data_type = [int, long]

class TextFlyProperty(FlyProperty):
  """A text property which will be stored in ``extra_dict``"""
  data_type = basestring

class ListFlyProperty(FlyProperty):
  """A list property which will be stored in ``extra_dict``"""
  data_type = list


def to_dict(model):
  # convert the model to a dict contains all its fields
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
  
  from common import auth
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
  """A reimplement for db.Model, use a faked ``delete()`` for debugging"""
  deleted = db.BooleanProperty(default=False)
  
  def to_dict(self):
    return to_dict(self)
  
  def delete(self, **kwargs):
    """docstring for def delete(self, **kwargs):"""
    self.deleted = True
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
    
    keys_only = kwargs.get('keys_only', False)
    
    query = super(Model, cls).all(keys_only=keys_only)\
                             .filter('deleted = ', False)

    for f in cls._properties.keys():
      if kwargs.has_key(f) and kwargs[f] is not None:
        query = query.filter(f, kwargs[f])
    
    return query
  
  @classmethod
  def gql(cls, query_string, *args, **kwds):
    """Deprecated method.
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
      model_class._fly_properties[attr] = prop
      prop.__property_config__(model_class, attr, dct)
  
class FlyPropertiedMeta(PropertiedClass):
  """docstring for FlyPropertiedClass"""
  _fly_properties = {}
  
  def __init__(cls, name, bases, dct):
    super(FlyPropertiedMeta, cls).__init__(name, bases, dct)
    
    _initialize_fly_properties(cls, name, bases, dct)
    

class FlyModel(Model):
  """Fot Model added extra_dict on Model to enable the usage of FlyProperty"""
  
  __metaclass__ = FlyPropertiedMeta
  
  extra_dict = DictProperty(default={})
  
  @classmethod
  def fly_properties(cls):
    """docstring for fly_properties"""
    return cls._fly_properties

class _MapQueryIterator(object):
  """Helper iterator for MapQuery"""
  def __init__(self, iterator, map_func):
    super(_MapQueryIterator, self).__init__()
    self.iterator = iterator
    self.map_func = map_func
  
  def __iter__(self):
    """docstring for __iter__"""
    return self
  
  def next(self):
    """docstring for next"""
    next_item = self.iterator.next()
    if next_item:
      next_item = self.map_func(next_item)
    return next_item
  

class MapQuery(object):
  """A map query that can map the results of the query using a given map
  function.
  
  map_func -- the mapping function
  query -- the original query
  allow_set -- if the mapping fuction supports result sets as input. E.g. 
  ``db.get()`` can accept both ``key`` and a list of ``key`` as its input.
  """
  def __init__(self, query, map_func, allow_set=False):
    super(MapQuery, self).__init__()
    self.query = query
    self._map_func = map_func
    self.allow_set = allow_set
  
  def map_results(self, results):
    """docstring for map_results"""
    import logging
    logging.debug("map results: %s", results)
    if self.allow_set or not isinstance(results, list):
      return self._map_func(results)
    else:
      return [self._map_func(x) for x in results]
  
  def filter(self, *args):
    return MapQuery(self.query.filter(*args), self.map_results)
  
  def order(self, *args):
    return MapQuery(self.query.order(*args), self.map_results)
  
  def get(self):
    result = self.query.get()
    if result:
      return self.map_results(result)
    return result;
  
  def fetch(self, *args, **kwargs):
    results = self.query.fetch(*args, **kwargs)
    return self.map_results(results)
  
  def count(self, *args):
    return self.query.count(*args)
  
  def __getitem__(self, *args):
    return self.map_results(self.query.__get_item__(*args))
  
  def __iter__(self):
    return _MapQueryIterator(self.query.__iter__(), self.map_results)
  
class GetQuery(MapQuery):
  """docstring for GetQuery"""
  def __init__(self, query):
    super(GetQuery, self).__init__(query, lambda x: db.get(x))

def delete(models):
  """docstring for delete"""
  if isinstance(models, db.Key) or isinstance(models, Model):
    models = [models]
    
  for model in models:
    if isinstance(model, db.Key):
      model = db.get(model)
    model.delete()