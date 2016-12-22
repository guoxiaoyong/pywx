# -*- coding: utf-8 -*-
import util

def check_content(reqmsg):
  matches_short = ['member id', 'memberid', u'会员号']
  matches_long = ['long member id', 'long memberid', u'长会员号']
  content = reqmsg['Content'].strip()
  if content in matches_short:
     return 1
  elif content in matches_long:
     return 2
  else:
     return False

def get_member_id(reqmsg):
  result = check_content(reqmsg)
  memberid = util.openid_to_memberid(reqmsg['FromUserName'])
  if result == 1:
    return memberid[:8]
  elif result == 2:
    return memberid


