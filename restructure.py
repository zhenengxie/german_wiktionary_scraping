""" Restructuring the german word database """

import dataset as ds
from progress.bar import Bar

DB = ds.connect('sqlite:///german.db')
DB_NEW = ds.connect('sqlite:///german2.db')

NOUN_BAR = Bar('nouns', max=len(DB['noun']))
for old_noun in DB['noun']:
    new_noun = {}

    new_noun['word'] = old_noun['word']
    new_noun['gender'] = old_noun['gender']
    new_noun['plural_ending'] = old_noun['plural_ending']
    new_noun['genitive_ending'] = old_noun['genitive_singular_ending']
    new_noun['plural'] = old_noun['plural']

    if old_noun['type'] == 'de-decl-adj+noun-f':
        new_noun['word'] = old_noun['word']
        new_noun['gender'] = 'adj'
        new_noun['plural_ending'] = None
        new_noun['genitive_ending'] = None
        new_noun['plural'] = None

    if old_noun['type'] != 'de-decl-adj+noun-m':
        DB_NEW['noun'].insert(new_noun)

    if new_noun['gender'] == 'f':
        new_noun['genitive_ending'] = None

    NOUN_BAR.next()
NOUN_BAR.finish()

ADJ_BAR = Bar('adjectives', max=len(DB['adjective']))
for old_adj in DB['adjective']:
    new_adj = {}

    new_adj['word'] = old_adj['word']
    new_adj['comparative'] = old_adj['comparative']
    new_adj['superlative'] = old_adj['superlative']

    DB_NEW['adjective'].insert(new_adj)

    ADJ_BAR.next()
ADJ_BAR.finish()

VERB_BAR = Bar('verbs', max=len(DB['verb']))
for old_verb in DB['verb']:
    new_verb = {}

    new_verb['word'] = old_verb['word']

    DB_NEW['verb'].insert(new_verb)

    VERB_BAR.next()
VERB_BAR.finish()

