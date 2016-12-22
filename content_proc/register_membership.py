# -*- coding: utf-8 -*-
# register membership
def check_content(reqmsg):
  matches = ['register', u'注册']
  content = reqmsg['Content'].strip()
  items = content.split()
  if (len(items) != 3 or
      items[0] not in matches):
    return False
  else:
    return item[1], item[2]


def register_membership(reqmsg):
  result = check_content(reqmsg)
  if result:
    #add_to_membership_table()
    return u"会员信息注册成功"
