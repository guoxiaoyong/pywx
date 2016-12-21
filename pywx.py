from flask import Flask
from flask import request
import logging
from config import Config
from util import *
from procmsg import *

Logger = logging.getLogger('weixin')
hdlr = logging.FileHandler('weixin.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
Logger.addHandler(hdlr)
Logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route('/xiaoyong', methods=['POST', 'GET'])
def xiaoyong():
  if request.method == 'GET':
    return verify_request(request, 'get request failed')
  elif request.method == 'POST':
    if not verify_request(request):
      return 'post request failed'

    request.get_data()
    raw_xml = request.data
    Logger.info(raw_xml)
    reqmsg = parse_xml_message(raw_xml)
    rspmsg = process_reqmsg(reqmsg)
    return rspmsg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
