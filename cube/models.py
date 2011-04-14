#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2011-04-12.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


import logging

from chrisw import db, gdb
from chrisw.core.memcache import cache_result

from common.auth import get_current_user, User, Guest
from conf import settings

class ThingSite(db.Model):
  """docstring for ThingSite"""
  avaliable_slots = db.IntegerProperty(default=0)

  def can_create_thing(self, user):
    """docstring for can_create_thing"""
    return False

  def create_thing(self, thing):
    """docstring for create_thing"""
    pass

class Thing(gdb.Entity):
  """docstring for Thing"""
  tags = db.StringListProperty(default=[])

  title = db.StringProperty(required=True)

  introduction = db.StringProperty(required=True)

  keyword_index = db.StringListProperty(required=True)

  # rank properties
  rank = db.FloatProperty(required=True)

  rank_1 = db.IntegerFlyProperty(required=True)
  rank_2 = db.IntegerFlyProperty(required=True)
  rank_3 = db.IntegerFlyProperty(required=True)
  rank_4 = db.IntegerFlyProperty(required=True)
  rank_5 = db.IntegerFlyProperty(required=True)

  def can_own(self, user):
    """docstring for can_own"""
    pass

  def has_owner(self, user):
    """docstring for has_owner"""
    pass

  def add_owner(self, user):
    """docstring for add_owner"""
    pass

  def can_want(self, user):
    """docstring for can_want"""
    pass

  def has_wanting_one(self):
    """docstring for has_wantor"""
    pass

  def add_wanting_one(self):
    """docstring for add_wanting_one"""
    pass


  def get_rank(self, user):
    """docstring for get_rank"""
    pass

  def add_rank(self, user, rank):
    """docstring for add_rank"""
    pass


  def update_rank_info(self):
    """docstring for update_rank_info"""
    pass

  def update_keyword_index(self):
    """docstring for update_keyword_index"""
    pass


class ThingComment(db.Entity):
  """docstring for ThingComment"""
  pass
#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2011-04-12.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


import logging

from chrisw import db, gdb
from chrisw.core.memcache import cache_result

from common.auth import get_current_user, User, Guest
from conf import settings

class ThingSite(db.Model):
  """docstring for ThingSite"""
  avaliable_slots = db.IntegerProperty(default=0)

  def can_create_thing(self, user):
    """docstring for can_create_thing"""
    return False

  def create_thing(self, thing):
    """docstring for create_thing"""
    pass

class Thing(gdb.Entity):
  """docstring for Thing"""

  creator = db.ReferenceProperty(User, required=True)

  title = db.StringProperty(required=True)

  introduction = db.StringProperty(required=True)
  
  photo_url = db.StringProperty(required=True)

  tags = db.StringListProperty(default=[])
  keyword_index = db.StringListProperty(required=True)

  # rank properties
  rank = db.FloatProperty(required=True)
  rank_counts = db.ListFlyProperty(default=[0] * 5)

  def can_own(self, user):
    """docstring for can_own"""
    pass

  def has_owner(self, user):
    """docstring for has_owner"""
    pass

  def add_owner(self, user):
    """docstring for add_owner"""
    pass

  def can_want(self, user):
    """docstring for can_want"""
    pass

  def has_wanting_one(self):
    """docstring for has_wantor"""
    pass

  def add_wanting_one(self):
    """docstring for add_wanting_one"""
    pass


  def get_rank(self, user):
    """docstring for get_rank"""
    pass

  def add_rank(self, user, rank):
    """docstring for add_rank"""
    pass


  def update_rank_info(self):
    """docstring for update_rank_info"""
    pass

  def rank_info(self):
    """docstring for rank_info"""
    pass

  def update_keyword_index(self):
    """docstring for update_keyword_index"""
    pass


class ThingComment(db.Entity):
  """docstring for ThingComment"""
  pass
#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2011-04-12.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


import logging

from chrisw import db, gdb
from chrisw.core.memcache import cache_result

from common.auth import get_current_user, User, Guest
from conf import settings

class ThingSite(db.Model):
  """docstring for ThingSite"""
  avaliable_slots = db.IntegerProperty(default=0)

  def can_create_thing(self, user):
    """docstring for can_create_thing"""
    return False

  def create_thing(self, thing):
    """docstring for create_thing"""
    pass

class Thing(gdb.Entity):
  """docstring for Thing"""
  tags = db.StringListProperty(default=[])

  title = db.StringProperty(required=True)

  introduction = db.StringProperty(required=True)

  keyword_index = db.StringListProperty(required=True)

  # rank properties
  rank = db.FloatProperty(required=True)

  rank_1 = db.IntegerFlyProperty(required=True)
  rank_2 = db.IntegerFlyProperty(required=True)
  rank_3 = db.IntegerFlyProperty(required=True)
  rank_4 = db.IntegerFlyProperty(required=True)
  rank_5 = db.IntegerFlyProperty(required=True)

  def can_own(self, user):
    """docstring for can_own"""
    pass

  def has_owner(self, user):
    """docstring for has_owner"""
    pass

  def add_owner(self, user):
    """docstring for add_owner"""
    pass

  def can_want(self, user):
    """docstring for can_want"""
    pass

  def has_wanting_one(self):
    """docstring for has_wantor"""
    pass

  def add_wanting_one(self):
    """docstring for add_wanting_one"""
    pass


  def get_rank(self, user):
    """docstring for get_rank"""
    pass

  def add_rank(self, user, rank):
    """docstring for add_rank"""
    pass


  def update_rank_info(self):
    """docstring for update_rank_info"""
    pass

  def update_keyword_index(self):
    """docstring for update_keyword_index"""
    pass


class ThingComment(db.Entity):
  """docstring for ThingComment"""
  pass
