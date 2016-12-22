# -*- coding: utf-8 -*-
import util

# register membership
def check_content(reqmsg):
  matches = [u'register', u'注册']
  content = reqmsg['Content'].strip()
  items = content.split()
  if (len(items) != 3 or
      items[0] not in matches):
    return False
  else:
    return items[1], items[2]

MESSAGE = u"""
会员信息注册成功
会员名: {}
联系电话: {}
会员号: {}
"""

def register_membership(reqmsg):
  result = check_content(reqmsg)
  if result:
    #add_to_membership_table()
    name = result[0]
    tel = result[1]
    memberid = util.openid_to_memberid(reqmsg['FromUserName'])
    return MESSAGE.format(name, tel, memberid[:8])
