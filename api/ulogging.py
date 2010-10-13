#!/usr/bin/env python
# encoding: utf-8
"""
ulogging.py

A logging module to record user's visiting paths. The records will be used for
profiling user behaviors. To compute the recommend groups and so on.

Created by Kang Zhang on 2010-10-12.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""


import logging


def log(url):
  """docstring for log"""
  user = get_current_user()
  
  logging.info("USER:[%d] Visited URL[%s]")


