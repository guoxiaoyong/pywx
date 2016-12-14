from flask import Flask
from flask import request
import hashlib
import xmltodict

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
    post_msg = xmltodict.parse(raw_xml)
    MyName = post_msg['xml']['ToUserName']
    CustomName = post_msg['xml']['FromUserName']
    CreateTime = post_msg['xml']['CreateTime']

    reply_msg = {'xml': {}}
    reply_msg['xml']['ToUserName'] = ToUserName
    reply_msg['xml']['FromUserName'] = FromUserName
    reply_msg['xml']['CreateTime'] = CreateTime
    reply_msg['xml']['MsgType'] = 'text'
    reply_msg['xml']['Content'] = 'How are you!'
    msg = xmltodict.unparse(reply_msg)
    return msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)