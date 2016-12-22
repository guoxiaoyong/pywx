#-*- coding: utf-8 -*-
import time
import xmltodict
import re
from util import *


# XML Message class
class XmlMessage(object):
  def __init__(self):
    self._msg = {}

  def add_field(self, fieldname, value):
    # check validity of fieldname and value
    self._msg[fieldname] = value

  def prepare(self):
    return xmltodict.unparse({'xml': self._msg})


# XML Response Message class
class XmlRspMessage(XmlMessage):
  def __init__(self, reqmsg):
    super(XmlRspMessage, self).__init__()  # python2
    self._msg['ToUserName'] = reqmsg['FromUserName']
    self._msg['FromUserName'] = reqmsg['ToUserName']
    self._msg['CreateTime'] = int(time.time())


def process_text_message(msg):
  rspmsg = XmlRspMessage(msg)
  rspmsg.add_field('MsgType', 'text')

  assert 'Content' in msg.keys()
  content_proc = ContentProc()
  result = content_proc.proc(msg)
  if result:
    rspmsg.add_field('Content', result)
    return rspmsg.prepare()
  else:
    return 'Message not processed!'


def process_image_message(msg):
  return 'successful'


def process_voice_message(msg):
  return 'successful'

def process_video_message(msg):
  return 'successful'

def process_short_video_message(msg):
  return 'successful'

def process_link_message(msg):
  return 'successful'

def process_location_message(msg):
  return 'successful'

def process_subsribe_event(msg):
  return 'successful'

def process_unsubsribe_event(msg):
  return 'successful'

def process_click_event(msg):
  return 'successful'

def process_view_event(msg):
  return 'successful'


def process_event_message(msg):
  event_handlers = {}
  event_handlers['subscribe'] = process_subscribe_event
  event_handlers['unsubscribe'] = process_unsubscribe_event
  event_handlers['CLICK'] = process_click_event
  event_handlers['VIEW'] = process_view_event

def process_reqmsg(msg):
  handlers = {}
  handlers['text'] = process_text_message
  handlers['image'] = process_image_message
  handlers['voice'] = process_voice_message
  handlers['video'] = process_video_message
  handlers['short_video'] = process_short_video_message
  handlers['link'] = process_link_message
  handlers['location'] = process_location_message
  handlers['event'] = process_event_message

  assert msg['MsgType'] in ['text', 'image',
  'voice', 'video', 'short_video', 'link', 'location', 'event']

  # need to handle unknown MsgType
  rspmsg = handlers[msg['MsgType']](msg)
  return rspmsg
