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
  
  def save(self, commit=True):
    """docstring for save"""
    
    fly_properties = self._meta.model.fly_properties()
    instance = self.instance
    
    clean_data = self._cleaned_data()
    
    if instance:
      for attr, fly_propertie in fly_properties.iteritems():
        if clean_data.has_key(attr):
          setattr(instance, attr, clean_data[attr])
    
    return super(ModelForm, self).save(commit)