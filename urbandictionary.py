import sys
import os
import random
import json
import requests
from pyquery import PyQuery


def retrieve_urbandictionary_define_page(term):
  url = 'http://www.urbandictionary.com/define.php'
  params = {'term': term}
  resp = requests.get(url, params=params)
  return resp.text.encode('utf8')


def parse_define_page(page_content=None, filename=None):
  if page_content:
    doc = PyQuery(page_content)
  else:
    doc = PyQuery(filename=filename)

  # word is not defined
  if doc('div.def-header > a.word').size() == 0:
    print "word not found."
    return None 

  words = [tag.text for tag in doc('div.def-header > a.word')]
  meanings = [tag.text for tag in doc('div.meaning')]
  examples = [tag.text for tag in doc('div.example')]
  res = [{'word': word.encode('utf8'),
          'meaning': meaning.encode('utf8'),
          'example': example.encode('utf8')}
         for word, meaning, example in zip(words, meanings, examples)] 
  return res
  

def format_parse_result(parsed):
  if not parsed:
    return None

  template = "word: {}\nmeaning: {}\nexample: {}\n"
  result = []
  n = random.randint(0, len(parsed)-1)
  entry = parsed[n]
  print type(entry['word'])
  try:
    return template.format(entry['word'], entry['meaning'], entry['example'])
  except UnicodeEncodeError:
    return template.format(entry['word'].encode('utf8'), entry['meaning'].encode('utf8'), entry['example'].encode('utf8'))


def lookup_urbandictionary(word):
  filepath = os.path.join('dict', word)
  if os.path.exists(filepath):
     parsed = json.load(open(filepath))
  else:
    html = retrieve_urbandictionary_define_page(word)
    parsed = parse_define_page(html)
    if parsed:
      with open(os.path.join('dict', word), 'wb') as outfile:
        json.dump(parsed, outfile)
  res = format_parse_result(parsed)
  return res or [{'word': 'NotFound', 'meaning': 'NoDefinition', 'example': 'None'}]


if __name__ == '__main__':
  print lookup_urbandictionary(sys.argv[1])
