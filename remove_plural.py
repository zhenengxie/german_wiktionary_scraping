import wiktextract as wk
import dataset as ds

DB = ds.connect('sqlite:///german.db')

NOUNS = DB['noun']

def add_noun(word, conjugation):
    if "n" in conjugation and conjugation["n"] == 'sg':
        data = NOUNS.find_one(word=word)
        if data:
            data["plural_ending"] = None
            data["plural"] = None
            NOUNS.update(data, ["word"])
            print("found one: " + word)

def word_cb(data):
    if 'conjugation' in data:
        if data['pos'] in ['noun', 'name']:
            for conjugation in data['conjugation']:
                add_noun(data['word'], conjugation)

wk.parse_wiktionary('enwiktionary.xml.bz2', word_cb, languages=['German'])
print("Yay, all parsed")
