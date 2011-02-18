#!/usr/bin/env python
# encoding: utf-8
"""
photo.py

Created by Kang Zhang on 2010-09-30.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore

from chrisw.core.handlers import api_enabled
from chrisw.core.action import *

from duser.auth import get_current_user
from api import errors

from front.models import *

def create_upload_url():
  """docstring for create_upload_url"""
  return blobstore.create_upload_url(r'/img/upload')

class PhotoHandler(blobstore_handlers.BlobstoreUploadHandler):
  
  def post(self):
    upload_files = self.get_uploads()  # 'file' is file upload field in the form
    photo_url = None
    back_url = self.request.headers.get('Referer','/') #self.request.get("back_url", "/")
    max_size = int(self.request.get("max_size", 102400))
    
    if not upload_files:
      return redirect(back_url)
    
    blob_info = upload_files[0]
    
    user = get_current_user()
    
    logging.debug(" Got user %s 's avatar %d", user.username, blob_info.size)
    
    if user and blob_info.size <= max_size:
      
      from google.appengine.api import images
      
      blob_key = str(blob_info.key())
      photo_url = images.get_serving_url(blob_key)
      
      photo = Photo(blob_key=blob_key, url=photo_url)
      photo.put()
        
    else:
      blob_info.delete()
      logging.error("User's avatar is too large for %s", user.username)

    import urllib
    if photo_url:
      back_url = back_url + "?image_url=" + urllib.quote_plus(photo_url)

    return redirect(back_url)
    
    

apps = [(r'/img/upload', PhotoHandler),
        ]