Introduction of Chrisw
======================
Chrisw is designed to be a flexible, group-based social network site running
on Google AppEngine, which shipped with an interactive web user interface.

A running version of Chrisw can be found at:

	http://daoshicha.appspot.com

Note that i18n is supported by Chrisw. It now supports both English and 
Chinese as the UI language.

Installation
============
Chrisw is not ready for release now. It's still under heavily development. 

All data is logged on the server. **Even you remove it from the site**. It's 
for debugging usage, please don't use it for production environment.

1. Generate your COOKIE_KEY using os.urandom(64) and store it in 
local_settings.py.

2. Modify the app.yaml to specify your appengine box.

3. Deploy it to server.

Settings 
========

Most settings can be config using the settings.py, and local_settings.py. The
options in local_settings.py are recommended to be changed in your production 
release.

License
=======


Chrisw will be distributed under GPL license or MIT license. We've not decided 
it yet.

About
=====

:Authors:
    Kang Zhang (jobo.zh AT gmail.com) http://home.kangzhang.org

:Version: 
	0.2

:Python: 
	2.5+