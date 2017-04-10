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
    return [{'word': 'Word not found',
             'meaning': 'No definition.',
             'example': 'None'}]

  words = [tag.text for tag in doc('div.def-header > a.word')]
  meanings = [tag.text for tag in doc('div.meaning')]
  examples = [tag.text for tag in doc('div.example')]
  return [{'word': word.encode('utf8'),
           'meaning': meaning.encode('utf8'),
           'example': example.encode('utf8')}
          for word, meaning, example in zip(words, meanings, examples)]


def format_parse_result(parsed):
  template = "word: {}\nmeaning: {}\nexample: {}\n"
  result = []
  print parsed
  print len(parsed)
  n = random.randint(0, len(parsed)-1)
  entry = parsed[n]
  return template.format(entry['word'], entry['meaning'], entry['example'])


def lookup_urbandictionary(word):
  filepath = os.path.join('dict', word)
  if os.path.exists(filepath):
     parsed = json.load(open(filepath))
  else:
    html = retrieve_urbandictionary_define_page(word)
    parsed = parse_define_page(html)
    with open(os.path.join('dict', word), 'wb') as outfile:
      json.dump(parsed, outfile)
  res = format_parse_result(parsed)
  return res


if __name__ == '__main__':
  parsed = parse_define_page(filename='nanjing.html')
  res = format_parse_result(parsed)
  print res
