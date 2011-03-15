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

    @cache("welcome-page-for-{user_name}s",time=60)
    def get(self, user_name):
      slogan = 'Hi %s, Welcome to Chrisw' % user_name
      return template('welcome.html', locals())


The above code declared a welcome page for user, it will be rendered using a
template called ``welcome.html`` and the ``locals()`` dict. The rendered page
will be cached for 60 seconds in memcache for each user.

Really Useful Storage API
-------------------------

::
  
  def get_recent_post_titles(user):
    """The example for MapQuery and Model.all()."""
    return db.MapQuery(Post.all(user=user), lambda x: x.title)\
      .order("-create_at").fetch(10)


The above code get all recent posts' titles by the given user. 

Pipline Rendering
-----------------

::

  def view(self, request):
    """The example for forward action."""
    # list group content and display group info
    # ...

    # add recommend groups widget in page    
    sidebar_widgets = [forward('/group/recommend').render()]
    
    return template('groupsite_display.html', locals())
  
  @cache_action('group-recommend-groups', 60)
  def recommend_groups(self):
    """Example for forwarded action and the cache syntax."""

    recommend_groups = [g for g in Group.all().fetch(10)]

    return template('window_recommend_groups', locals())


The above code creates a view for the given group. The recommend groups are 
list in a widget on the page. The rendering of the widget are forwarded to the
``recommend_groups`` handler, while the rendered html will be cached for 60
seconds in memcache. The following figure show the workflow of pipeline 
rendering.

.. image:: https://github.com/kangzhang/chrisw/blob/develop/docs/PipelineRendering.png?raw=true



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

Chrisw is going to be distributed under GPL license or MIT license. I've not 
decided it yet.

About
=====

:Authors:
    Kang Zhang (jobo.zh AT gmail.com) http://home.kangzhang.org

:Version: 
	0.3

:Python: 
	2.5+