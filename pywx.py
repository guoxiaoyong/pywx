import sys
import flask

from util import LOG
from procmsg import process_reqmsg

app = flask.Flask(__name__)

@app.route('/xiaoyong', methods=['POST', 'GET'])
def xiaoyong():
  if request.method == 'GET':
    return verify_request(request, 'get request failed')
  elif request.method == 'POST':
    if not verify_request(request):
      return 'post request failed'

    flask.request.get_data()
    raw_xml = flask.request.data
    LOG.info(raw_xml)
    reqmsg = parse_xml_message(raw_xml)
    rspmsg = process_reqmsg(reqmsg)
    return rspmsg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
