# -*- coding: utf-8 -*-
import time

USAGE = u"""
book/预定/预约 时间 课程
时间: YYYYMMDD, 例如20170324, 只能预约未来1个月的课程
课程: 钢琴，绘画，手工
"""

def check_content(reqmsg):
  content = reqmsg['Content'].strip()
  matches = [u'book', u'预定', u'预约']
  items = content.split()
  if (len(items) != 3 or
      items[0] not in matches):
    return False
  else:
    return items[1], items[2]


def check_date(date_str):
  if len(date_str) != 8:
    return False

  if not date_str.isdigit():
    return False

  book_time = time.mktime(time.strptime(date_str,'%Y%m%d'))
  diffsec = book_time - time.time()
  if diffsec < 0 or diffsec > 24*3600*30:
    return False
  else:
    return True


def make_booking(reqmsg):
  classes = [u'钢琴', u'绘画', u'手工']
  result = check_content(reqmsg)
  if result:
    if result[1] not in classes:
      return u'Unknown program' +  USAGE
    elif not check_date(result[0]):
      return u'Wrong booking time' + USAGE
    else:
      return u'预约成功'
