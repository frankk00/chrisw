#!/usr/bin/env python
# encoding: utf-8
"""
css_pig.py

Could be use with 
  http://www.cleancss.com/

Created by Kang Zhang on 2011-04-08.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

import sys
import getopt


help_message = '''
Css formatter tool for Chrisw.
'''

def format(css, out):
  """docstring for format"""
  import cssutils
  
  sheet = cssutils.parseString(css)
  rules = sheet.cssRules
  
  rules.sort(key=lambda r: r.cssText.split('{')[0] if r.cssText else '' )
  
  rule_num = len(rules)
  
  index_wrapper = [0]
  
  def write_rule(prefix, rule):
    """docstring for write_rule"""
    index_wrapper[0] += 1
    if rule.cssText: # skip the empty style
      lines = rule.cssText.splitlines()
      lines[0] = prefix + lines[0]
      lines[-1] = prefix + lines[-1]
      
      for i in range(1, len(lines) -1):
        lines[i] = prefix + '  ' + lines[i]
      
      for line in lines:
        out.write(line + '\n')
    
  
  def process_rule(selector_prefix="", print_prefix=""):
    """docstring for write_rule"""
    index = index_wrapper[0]
    
    if index >= rule_num:
      return
    
    while index < rule_num:
      rule = rules[index]
      
      if isinstance(rule, cssutils.css.CSSStyleRule):
        selector_name = rule.selectorList[0].selectorText.strip()
        
        if selector_name.startswith(selector_prefix) and \
          len(selector_name) > len(selector_prefix) and \
          selector_name[len(selector_prefix)] in (':', ' '):
          
          new_print_prefix = print_prefix + "  "
          new_selector_prefix = selector_name
          
          write_rule(new_print_prefix, rule)
          
          process_rule(new_selector_prefix, new_print_prefix)
        
        elif print_prefix:
          return # not suitable for this indent
        else:
          out.write('\n')
          write_rule(print_prefix, rule)
          
          selector_prefix = selector_name
      else:
        # zero indent
        write_rule(print_prefix, rule)
        
      index = index_wrapper[0]
  
  process_rule()

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg


def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
    except getopt.error, msg:
      raise Usage(msg)
  
    verbose = False
    output = None
    
    # option processing
    for option, value in opts:
      if option == "-v":
        verbose = True
      if option in ("-h", "--help"):
        raise Usage(help_message)
      if option in ("-o", "--output"):
        output = value
    
    path = args[0]
    
    out = sys.stdout
    if output: out = open(output, 'w')
    
    css = open(path).read()
    
    format(css, out)
    
  except Usage, err:
    print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
    print >> sys.stderr, "\t for help use --help"
    return 2


if __name__ == "__main__":
  sys.exit(main())
