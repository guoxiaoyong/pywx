import sys
import os
import flask

from util import LOG
from procmsg import process_reqmsg
from procmsg import verify_request
from procmsg import parse_xml_message

app = flask.Flask(__name__)

@app.route('/xiaoyong', methods=['POST', 'GET'])
def xiaoyong():
  if flask.request.method == 'GET':
    return verify_request(flask.request, 'get request failed')
  elif flask.request.method == 'POST':
    if not verify_request(flask.request):
      return 'post request failed'

    flask.request.get_data()
    raw_xml = flask.request.data
    LOG.info(raw_xml)
    reqmsg = parse_xml_message(raw_xml)
    rspmsg = process_reqmsg(reqmsg)
    return rspmsg


def load_resource(name):
  path = os.path.join(os.path.dirname(__file__), 'blog', name)
  if os.path.exists(path):
    with open(path) as infile:
      content = infile.read();
    return content
  

@app.route('/')
def index():
  return load_resource('index.html')

@app.route('/<blog_page>')
def blog(blog_page):
  return load_resource(blog_page)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(sys.argv[1]))
