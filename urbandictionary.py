import sys
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
  for entry in parsed:
    result.append(template.format(
        entry['word'], entry['meaning'], entry['example']))
  return '\n\n'.join(result)


def lookup_urbandictionary(word):
  html = retrieve_urbandictionary_define_page(word)
  parsed = parse_define_page(html)
  return format_parse_result(parsed)

print lookup_urbandictionary(sys.argv[1])
