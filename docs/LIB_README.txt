"""
LIB_README.txt

Created by Kang Zhang on 2010-09-22.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

"""
Demostration for the session lib
"""

from lib.gaesessions import get_current_session
session = get_current_session()
if session.is_active():
    c = session.get('counter', 0)
    session['counter'] = c + 1
    session['blah'] = 325
    del session.blah  # remove 'blah' from the session
    # model instances and other complex objects can be stored too

    # If you don't care if a particular change to the session is persisted
    # to the datastore, then you can use the "quick" methods.  They will
    # only cause the session to be stored to memcache.  Of course if you mix
    # regular and quick methods, then everything will be persisted to the
    # datastore (and memcache) at the end of the request like usual.
    session.set_quick('x', 9)
    x = session.get('x')
    x = session.pop_quick('x')

# ...
# when the user logs in, it is recommended that you rotate the session ID (security)
session.regenerate_id()
