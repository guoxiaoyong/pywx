import pdb
import os
import time
import yaml
import requests
import pyqrcode
import xmltodict
from config import Config


# get url of weixin API
def get_api_url(target):
  url = 'https://api.weixin.qq.com/cgi-bin/'
  return url + target


def update_access_token():
  url = get_api_url('token')
  params = {}
  params['grant_type'] = 'client_credential'
  params['appid'] = Config.APPID
  params['secret'] = Config.APPSECRET
  req = requests.get(url, params=params)
  if req.status_code == 200:
    # In case there is no json content,
    # this line raises exception
    query_result = req.json()
    if 'errcode' in query_result.keys():
      raise Exception('Failed to query')
    else:
      with open(Config.ACCESS_TOKEN_FILE, 'wb') as yaml_file:
        # Use unix time, timezone is irrelavant here.
        query_result['update_time'] = time.time()
        yaml_file.write(yaml.safe_dump(query_result,
                                       default_flow_style=False))
  else:
    raise Exception('Failed to get access_token')


def get_access_token():
  if not os.path.exists(Config.ACCESS_TOKEN_FILE):
    update_access_token()
    return get_access_token()

  with open(Config.ACCESS_TOKEN_FILE) as yaml_file:
    token = yaml.load(yaml_file)
    expire_time = token['expires_in'] + token['update_time']
    if (time.time() < expire_time - 100):
      return token['access_token']
    else:
      update_access_token()
      return get_access_token()


def update_server_list():
  url = get_api_url('getcallbackip')
  params = {}
  params['access_token'] = get_access_token()
  req = requests.get(url, params=params)
  if req.status_code == 200:
     # In case there is no json content,
     # this line raises exception
     return req.json()
  else:
    raise Exception('Failed to get access_token')


def from_human_readable(hnum):
  for n, char in enumerate(hnum):
    if not char.isdigit():
      break
  assert n > 0
  num = int(hnum[:n])
  unit = hnum[n:]
  if unit == 'G':
    return num*1024*1024*1024
  if unit == 'M':
    return num*1024*1024
  if unit == 'K':
    return num*1024
  assert False


def check_upload_file(filepath):
  upload_policy = """
  image jpg jpeg gif png 2M
  voice amr mp3 2M
  video mp4 10M
  thumb thumb 64K
  """
  lines = upload_policy.split('\n')
  type2ext = {}
  for line in lines:
    items = line.split()
    if items:
      size_limit = from_human_readable(items[-1])
      type2ext[items[0]] = {'ext': items[1:-1],
                            'size_limit': size_limit}

  ext2type = {}
  for filetype, value in type2ext.items():
    for ext in value['ext']:
      ext2type[ext] = filetype

  if not os.path.exists(filepath):
    return False

  ext = filepath.split('.')[-1]
  if ext not in ext2type.keys():
    return False

  filesize = os.path.getsize(filepath)
  filetype = ext2type[ext]
  if filesize > type2ext[filetype]['size_limit']:
    return False

  return filetype


def upload_file(filepath):
  filetype = check_upload_file(filepath)
  if not filetype:
    return False

  url = get_api_url('media/upload')
  params = {}
  params['access_token'] = get_access_token()
  params['type'] = filetype
  with open(filepath, 'rb') as the_file:
    files = {'media': the_file}
    req = requests.post(url, params=params, files=files)
  if req.status_code == 200:
    upload_result = req.json()
    if 'errcode' in upload_result.keys():
      print upload_result
      return False
    else:
      return upload_result
  else:
    return False


def verify_request(request, fail_rsp=None):
  signature = request.args.get('signature', None)
  timestamp = request.args.get('timestamp', None)
  nonce = request.args.get('nonce', None)
  echo = request.args.get('echostr', None)

  if signature is None or timestamp is None or nonce is None:
    return False

  if request.method == 'GET' and echo is None:
    return False

  joined = ''.join(sorted([Config.TOKEN, timestamp, nonce]))
  Signature = hashlib.sha1(joined).hexdigest()
  if (Signature == signature):
    if request.method == 'GET':
      return echo
    else:
      return True
  else:
    return fail_rsp


def parse_xml_message(xml):
  msg = xmltodict.parse(xml)
  return msg['xml']

def gen_qrcode(content):
  qrcode = pyqrcode.create(content)
  qrcode.png('/tmp/qr.png', scale=3)

def get_member_id(openid):
  return hashlib.sha1(openid).hexdigest()

if __name__ == "__main__":
  #gen_qrcode('hello world!')
  #pdb.set_trace()
  print upload_file('/tmp/qr.png')
  #print update_server_list()
