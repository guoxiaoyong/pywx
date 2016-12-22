# -*- coding: utf-8 -*-
import util

def check_content(reqmsg):
  matches = ['member id', 'memberid', u'会员号']
  content = reqmsg['Content'].strip()
  return content in matches

def get_member_id(reqmsg):
  if check_content(reqmsg):
    return util.openid_to_memberid(reqmsg['FromUserName'])
