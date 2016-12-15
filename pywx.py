from flask import Flask
from flask import request
import hashlib
import xmltodict
import random
import logging

Logger = logging.getLogger('weixin')
hdlr = logging.FileHandler('weixin.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
Logger.addHandler(hdlr)
Logger.setLevel(logging.INFO)

app = Flask(__name__)
_TOKEN = 'guoxiaoyong'

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


class Quotes(object):
  def __init__(self):
    with open('quotes/quotes_cn.txt') as fd:
      self._quotes = fd.readlines()

  def random(self):
    num = random.randint(1, len(self._quotes)-1)
    return self._quotes[num]

Rand_Quotes = Quotes()
with open('quotes/welcome.txt') as fd:
  Welcome_Msg = fd.read().decode('utf8')

@app.route('/xiaoyong', methods=['POST', 'GET'])
def xiaoyong():
  # weixin's way for the weixin server
  # to verify the custom server
  if request.method == 'GET':
    signature = request.args.get('signature', None)
    timestamp = request.args.get('timestamp', None)
    nonce = request.args.get('nonce', None)
    echo = request.args.get('echostr', None)
    weixin_string = ''.join(sorted([_TOKEN, timestamp, nonce]))
    my_signature = hashlib.sha1(weixin_string).hexdigest()
    if (my_signature == signature):
      return echo
  elif request.method == 'POST':
    request.get_data()
    raw_xml = request.data
    Logger.info(raw_xml)
    post_msg = xmltodict.parse(raw_xml)
    ServerName = post_msg['xml']['ToUserName']
    ClientName = post_msg['xml']['FromUserName']
    CreateTime = post_msg['xml']['CreateTime']

    reply_msg = {'xml': {}}
    reply_msg['xml']['ToUserName'] = ClientName
    reply_msg['xml']['FromUserName'] = ServerName
    reply_msg['xml']['CreateTime'] = CreateTime
    reply_msg['xml']['MsgType'] = 'text'

    if (post_msg['xml']['MsgType'] == 'event' and
        post_msg['xml']['Event'] == 'subscribe'):
      reply_msg['xml']['Content'] = Welcome_Msg
    else:
      reply_msg['xml']['Content'] = Rand_Quotes.random().decode('utf8')
    msg = xmltodict.unparse(reply_msg)
    return msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
