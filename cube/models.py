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

OWNER = 'has-thing-owner'
WANTING_ONE = 'has-thing-wanting-one'
RANK = 'has-been-thing-rank-by'
DIG = 'has-been-thing-comment-dig-by'


class ThingSite(db.Model):
  """docstring for ThingSite"""
  avaliable_slots = db.IntegerProperty(default=0)

  def can_create_thing(self, user):
    """docstring for can_create_thing"""
    return self.avaliable_slots > 0

  def create_thing(self, thing):
    """docstring for create_thing"""
    pass

  @classmethod
  @cache_result('%s-site', 240)
  def get_instance(cls):
    """docstring for get_instance"""
    instance = super(ThingSite, cls).all().get()
    if not instance:
      instance = cls()
      instance.put()

    return instance


class Thing(gdb.Entity):
  """docstring for Thing"""
  creator = db.ReferenceProperty(User, required=True)

  title = db.StringProperty(required=True)

  introduction = db.StringProperty(required=True)

  photo_url = db.StringProperty(required=True)

  tags = db.StringListProperty(default=[])

  index_fields = ['title']
  keyword_index = db.StringListProperty(required=True)

  # rank properties
  rank = db.FloatProperty(required=True)
  rank_counts = db.ListFlyProperty(default=[0] * 6)
  rank_count_sum = db.IntegerFlyProperty(default=0)


  def can_own(self, user):
    """docstring for can_own"""
    return user.is_not_guest() and not self.has_owner(user)

  def has_owner(self, user):
    """docstring for has_owner"""
    return self.has_link(OWNER, user)

  def add_owner(self, user):
    """docstring for add_owner"""
    self.link(OWNER, user)

  def remove_owner(self, user):
    """docstring for remove_owner"""
    self.unlink(OWNER, user)


  def can_want(self, user):
    """docstring for can_want"""
    return user.is_not_guest() and not self.has_wanting_one(user) and not \
      self.has_owner(user)

  def has_wanting_one(self, user):
    """docstring for has_wantor"""
    return self.has_link(WANTING_ONE, user)

  def add_wanting_one(self, user):
    """docstring for add_wanting_one"""
    self.link(WANTING_ONE, user)

  def remove_wanting_one(self, user):
    """docstring for remove_wanting_one"""
    self.unlink(WANTING_ONE, user)

  def can_rank(self, user):
    """docstring for can_rank"""
    return user.is_not_guest() and not self.get_rank(user) is None

  def get_rank(self, user):
    """docstring for get_rank"""
    return self.get_link_attr(RANK, user)

  def add_rank(self, user, rank):
    """docstring for add_rank"""
    if int(rank) in range(1, 6):
      self.link(RANK, user, link_attr=rank)
    else:
      raise Exception("Rank must between 1 to 5")

  def can_comment(self, user):
    """docstring for can_comment"""
    pass

  def has_comment_by(self, user):
    """docstring for has_comment_by"""
    pass

  def get_comment(self, user):
    """docstring for get_comment_by"""
    pass

  def add_comment(self, user, comment):
    """docstring for add_comment"""
    pass

  def remove_comment(self):
    """docstring for remove_comment"""
    pass

  def update_rank_info(self):
    """docstring for update_rank_info"""
    self.rank = 0.0
    self.rank_count_sum = 0

    for i in range(1, 6):
      rank_count = self.get_targets(RANK, User, link_attr=str(i)).count()
      self.rank_counts[i] = rank_count
      self.rank += rank_count * 1.0 * i
      self.rank_count_sum += rank_count

    self.rank = self.rank / self.rank_count_sum

  @property
  def rank_info(self):
    """docstring for rank_info"""
    rank = self.rank
    rank_count_sum = self.rank_count_sum
    ranks = zip(range(1, 6), rank_counts)
    return locals()

  def update_keyword_index(self):
    """docstring for update_keyword_index"""
    pass


class ThingComment(db.Entity):
  """docstring for ThingComment"""
  author = db.ReferenceProperty(User)
  content = db.TextPropery(required=True)

  thing = db.ReferenceProperty(Thing)
  thing_type = db.StringProperty(required=True)

  ups = db.IntegerFlyProperty(default=0)
  downs = db.IntegerFlyProperty(default=0)

  def can_dig(self, user):
    """docstring for can_dig"""
    return user.is_not_guest() and self.has_digged_by(user)

  def has_digged_by(self, user):
    """docstring for has_digged"""
    return self.has_link(DIG, user)

  def up(self, user):
    """docstring for up"""
    self.link(DIG, user, link_attr=str(1))
    self.update_digs()

  def down(self, user):
    """docstring for down"""
    self.link(DIG, user, link_attr=str(-1))
    self.update_digs()

  def update_digs(self):
    """docstring for update_digs"""
    self.ups = self.targets(DIG, User, link_attr=str(1)).count()
    self.downs = self.targets(DIG, User, link_attr=str(-1)).count()
