#!/usr/bin/env python
#
# Copyright belongs to the contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# config the django's settings, is needed by django 1.1 but not 0.96
# explain from django's doc:
#   It boils down to this: Use exactly one of either configure() or 
#   DJANGO_SETTINGS_MODULE. Not both, and not neither.
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# patch for google's app_engine laucher, the shipped django's version is
# 0.96, need this hack if you are going to run it in your local server.
if os.environ.get('SERVER_SOFTWARE','').startswith('Devel'):
  sys.path.insert(0, "/Applications/GoogleAppEngineLauncher.app/Contents/"
                     "Resources/GoogleAppEngine-default.bundle/Contents/"
                     "Resources/google_appengine/lib/django/")

# patch from google
# refer to http://code.google.com/appengine/docs/python/tools/libraries.html#Django
from google.appengine.dist import use_library
use_library('django', '1.1')

import logging, settings

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template


def main():
  sys.path += settings.LIB_DIRS

  # for k in [k for k in sys.modules if k.startswith('django')]:
  #     del sys.modules[k]
  
  # patchs for django 0.96, should be remove for 1.1
  from django.conf import settings as djsettings
  djsettings.TEMPLATE_DIRS += settings.TEMPLATE_DIRS
  djsettings.INSTALLED_APPS += settings.INSTALLED_APPS
  
  # try to fix SystemError: Parent module 'django.utils.translation' not loaded
  djsettings._target = None
  
  import front, group
  application = webapp.WSGIApplication( front.apps + group.apps, 
                                        debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
