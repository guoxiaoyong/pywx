# -*- coding: utf-8 -*-
from urbandictionary import lookup_urbandictionary

USAGE = u"""
lookup word
"""

def check_content(reqmsg):
  content = reqmsg['Content'].strip()
  words = content.split()
  if words[0] == "lookup":
    return ' '.join(words[1:])


def lookup(reqmsg):
  term = check_content(reqmsg)
  if term:
    print term
    return lookup_urbandictionary(term);
