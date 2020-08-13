#!/usr/bin/python3
import xml.etree.ElementTree as ET

input_file = 'enwiktionary-20200801-pages-meta-current.xml'
all_words_output_file = 'english_words.txt'
game_words_output_file = 'english_game_words.txt'
game_words_ci_output_file = 'english_game_words_case_insensitive.txt'

namespace = '{http://www.mediawiki.org/xml/export-0.10/}'

def is_word(s):
  special_word_characters = ['\'','-']
  for letter in s:
    if not (letter.isalpha() or letter in special_word_characters):
      return False
  return True

def is_game_word(s):
  if (any(letter.lower() not in "abcdefghijklmnopqrstuvwxyz" for letter in s)):
    return False
  elif s.isupper():
    return False
  return True

def iterative_parse():
  english_words = []
  current_page = {}
  tags_to_parse = [
    namespace + tag for tag in ['page','mediawiki','title','revision','text']
  ]
  for event, elem in ET.iterparse(input_file, events=('start','end')):
    if (event == 'start'):
      if (elem.tag == namespace + 'page'):
        current_page = {}
      if (elem.tag not in tags_to_parse):
        elem.clear()
    elif (event == 'end'):
      if (elem.tag == namespace + 'page'):
        if (
            (current_page['title'] and is_word(current_page['title'])) and
            (current_page['text'] and '==English==' in current_page['text'])
        ):
          english_words.append(current_page['title'])
          if (len(english_words) % 100000 == 0):
            print(len(english_words))
        current_page = {}
      elif (elem.tag == namespace + 'title'):
        current_page['title'] = elem.text
      elif (elem.tag == namespace + 'text'):
        current_page['text'] = elem.text
      elem.clear()
  return english_words

def write_output(words, filename):
  with open(filename, 'w') as f:
    f.write("\n".join(words))
    f.write("\n")
  print(f"Wrote {len(words)} words to {filename}")

def parse_wiktionary_data():
  english_words = iterative_parse()
  english_words.sort()
  write_output(english_words, all_words_output_file)
  game_words = [word for word in english_words if is_game_word(word)]
  write_output(game_words, game_words_output_file)
  game_words_ci = list(set(word.lower() for word in game_words))
  game_words_ci.sort()
  write_output(game_words_ci, game_words_ci_output_file)
  
if __name__ == "__main__":
  parse_wiktionary_data()
