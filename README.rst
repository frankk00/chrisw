Introduction of Chrisw
======================
Chrisw is designed to be a flexible, group-based social network site running
on Google AppEngine, which shipped with an interactive web user interface.

A running version of Chrisw can be found at:

	http://daoshicha.kangzhang.org
	or
	http://daoshicha.appspot.com

It now supports:

* a group-based community 
* i18n. (It now supports both English and Chinese as the UI language).
* a storage designed for speed and large scale
* more features are coming :-P

Chrisw is not only a website but also a macro web framework for Google 
AppEngine based application development. 


It contains:

AOP Web Development Workflow
----------------------------

::

  class WelcomeHandler(handlers.RequestHandler):

    @cache("welcome-page-for-{user.name}s",time=60)
    def get(self, user):
      slogan = 'Hi %s, Welcome to Chrisw' % user.name
      return template('welcome.html', locals())


The above code declared a welcome page for user, it will be rendered using a
template called ``welcome.html`` and the ``locals()`` dict. The rendered page
will be cached for 60 seconds in memcache for each user.

and it also contains:

* an implemented authentication and authorization module
* a set of helper classes for daily development 
* an integrated gaesession in the framework
* some useful hotfixs for Google AppEngine's django runtime
* a privacy sensitive storage module
* some basic css resets  


Installation
============
**Chrisw is not ready for deployment now. It's still under heavily development.** 

Instructions:

1. Generate your ``COOKIE_KEY`` using ``os.urandom(64)`` and store it in 
   ``local_settings.py``.

2. Modify the ``app.yaml`` to specify your appengine box.

3. Deploy it to server.

4. Change the ``DEBUG`` in ``local_settings.py`` to ``False``

Settings 
========

Most settings can be config using the ``settings.py``, and ``local_settings.py``
The options in ``local_settings.py`` are recommended to be changed in your 
production release.

Documentation
=============

For more document, you can refer to

    https://github.com/kangzhang/chrisw/wiki

About Chrisw2
=============

Yes, **Chrisw2** is under development. The mission of Chrisw2 is becoming a 
scalable, fast, module based web framework. Once it has been done, we will 
re-implement Chrisw using it.

Chrisw and Chrisw2 are both under construction at current time. The team for
Chrisw2 is larger and full of enthusiasm. Chrisw2 will be published when it 
reaches the first milestone. If you've any idea of that, contact 
jobo.zh AT gmail.com without any hesitate. :-)  

License
=======

Chrisw is going to be distributed under GPL license or MIT license. We've not 
decided it yet.

About
=====

:Authors:
    Kang Zhang (jobo.zh AT gmail.com) http://home.kangzhang.org

:Version: 
	0.3

:Python: 
	2.5+