#!/usr/bin/env python
# encoding: utf-8
"""
djangoforms.py

Created by Kang Zhang on 2011-03-12.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


from google.appengine.ext.db import djangoforms

class ModelForm(djangoforms.ModelForm):
  """docstring for ModelForm"""
  def __init__(self, **kwargs):
    object_data = {}
    opts = self._meta
    instance = kwargs.get('instance', None)
    
    if instance is not None:
      for name, prop in instance.fly_properties().iteritems():
        if name in opts.fields:
          object_data[name] = getattr(instance, name)
        
    initial = kwargs.get('initial', {})
    initial.update(object_data)
    
    kwargs['initial'] = initial
    
    super(ModelForm, self).__init__(**kwargs)
    
  def save(self, commit=False):
    """docstring for save"""
    
    instance = super(ModelForm, self).save(commit)
    
    if instance:
      
      fly_properties = self._meta.model.fly_properties()
      clean_data = self._cleaned_data()
      
      for attr, fly_propertie in fly_properties.iteritems():
        if clean_data.has_key(attr):
          setattr(instance, attr, clean_data[attr])
      if commit:
        instance.put()
    
    return instance