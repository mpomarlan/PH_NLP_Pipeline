import nltk
from nltk.tokenize import word_tokenize
from xml.etree import ElementTree
from pprint import pprint
from nltk.corpus import framenet as fn

import json

def frame_idname_list(lemma):
    frames = fn.frames_by_lemma(lemma)
    retq = []
    for f in frames:
        retq.append((f["ID"], f["name"]))
    return tuple(retq)

punct = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

sent = input("Enter the sentence: ")

with open('morph.xml', 'rt') as f:
    tree = ElementTree.parse(f)

with open('types.xml', 'rt') as f2:
    tree2 = ElementTree.parse(f2)

no_punct = ""
for char in sent:
   if char not in punct:
       no_punct = no_punct + char

word_list = word_tokenize(no_punct.lower())
i=0

postagged =  nltk.pos_tag(word_list)

frames = []
for x in word_list:
    frames.append((x, frame_idname_list(x)))

ccg_pos = []
for node in tree.iter('entry'):
    for x in word_list:
      name = node.attrib.get('word')
      pos = node.attrib.get('pos')
      if name == x:
           ccg_pos.append((x,str(pos)))

ccg_class = []
for node in tree.iter('entry'):
    for x in word_list:
      name = node.attrib.get('word')
      cl = node.attrib.get('class')

      if name == x:
           ccg_class.append ((x, str(cl)))

ccg_parent = []
for node in tree.iter('entry'):
  for node2 in tree2.iter('type'):
    for x in word_list:
      name = node.attrib.get('word')
      cl = node.attrib.get('class')
      types= node2.attrib.get('name')
      parents = node2.attrib.get('parents')

      if name==x and types ==cl:
           ccg_parent.append((x, str(parents)))

analysis = {"words": word_list, "nltk_pos": postagged, "frames": frames, "ccg_pos": ccg_pos, "class": ccg_class, "parent": ccg_parent}
output = {"analysis": analysis}

json_output = json.dumps(output)

print(json_output)

