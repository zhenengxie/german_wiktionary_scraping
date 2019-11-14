import wiktextract as wk
import dataset as ds
from collections import defaultdict
import json

"""
DB = ds.connect('sqlite:///german.db')

ADJS = DB['adjective']
NOUNS = DB['noun']
VERBS = DB['verb']
"""

conj_types = defaultdict(lambda: defaultdict(int))

def word_cb(data):
    if 'conjugation' in data:
        for conjugation in data['conjugation']:
            conj_types[data['pos']][conjugation['template_name']] += 1

wk.parse_wiktionary('enwiktionary.xml.bz2', word_cb, languages=['German'])

with open('test.json', 'w') as f:
    f.write(json.dumps(conj_types))
