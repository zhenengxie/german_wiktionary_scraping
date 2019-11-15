import wiktextract as wk
import dataset as ds

DB = ds.connect('sqlite:///german.db')

ADJS = DB['adjective']
NOUNS = DB['noun']
VERBS = DB['verb']

def get_default(conjugation, key, default):
    if key in conjugation:
        if conjugation[key] != '':
            return conjugation[key]
    return default

def get_bool(conjugation, key):
    if key in conjugation:
        if conjugation[key] != '':
            return True
    return False

def add_verb(word, conjugation):
    verb = {'word': word}
    verb['type'] = conjugation['template_name']

    def get_auxillary(key):
        if key in conjugation:
            aux = conjugation[key]
            if aux == 'h' or aux == 'haben' or aux == '':
                return 'h'
            if aux == 's' or aux == 'sein':
                return 's'
            if aux == 'hs' or aux == 'sh':
                return 'hs'
        else:
            return 'h'

    if verb['type'] == 'de-conj-strong':
        verb['present_stem'] = get_default(conjugation, '1', '')
        verb['e_on_present_second_third'] = get_bool(conjugation, '5')
        verb['past_stem'] = get_default(conjugation, '2', '')
        verb['past_participle'] = get_default(conjugation, '3', '')
        verb['auxillary_verb'] = get_auxillary('4')
        verb['present_second_third_stem'] = get_default(conjugation, '6', verb['present_stem'])
        verb['conjunctive_ii_stem'] = get_default(conjugation, '7', verb['past_stem'])
        verb['append_te_past_stem'] = get_bool(conjugation, '8')
        verb['no_e_imperative'] = get_bool(conjugation, '9')
        verb['seperable_prefix'] = get_default(conjugation, '10', '')
        verb['seperable_prefix_ii'] = ''
        verb['imperative_uses_infinite_vowel'] = get_bool(conjugation, '11')
        verb['esset_stem_ending'] = get_bool(conjugation, '12')
        verb['present_second_ends_t'] = False

    if verb['type'] in ['de-conj-weak', 'de-conj-weak-ern', 'de-conj-weak-eln']:
        verb['present_stem'] = get_default(conjugation, '1', '')
        verb['e_on_present_second_third'] = get_bool(conjugation, '4')
        verb['past_stem'] = verb['present_stem']
        if verb['e_on_present_second_third']:
            verb['past_participle'] = 'ge{0}et'.format(verb['present_stem'])
        else:
            verb['past_participle'] = 'ge{0}t'.format(verb['present_stem'])
        verb['auxillary_verb'] = get_auxillary('3')
        verb['present_second_third_stem'] = verb['present_stem']
        verb['conjunctive_ii_stem'] = verb['present_stem']
        verb['append_te_past_stem'] = True
        verb['no_e_imperative'] = False
        verb['seperable_prefix'] = get_default(conjugation, '6', '')
        verb['seperable_prefix_ii'] = ''
        verb['imperative_uses_infinite_vowel'] = True
        verb['esset_stem_ending'] = False
        verb['present_second_ends_t'] = get_bool(conjugation, '5')

    if verb['type'] in ['de-conj-weak', 'de-conj-weak', 'de-conj-weak-ern', 'de-conj-weak-eln']:
        VERBS.insert_ignore(verb, ['word'])

def add_noun(word, conjugation):
    noun = {'word': word, 'type': conjugation['template_name']}

    def get_plural(key):
        if 'pl' in conjugation:
            noun['plural'] = conjugation['pl']
        else:
            noun['plural_ending'] = get_default(conjugation, key, '')

    def get_dative_plural():
        if 'datpl' in conjugation:
            noun['dative_plural'] = conjugation['datpl']

    if noun['type'] in ['de-decl-noun-m', 'de-decl-adj+noun-m']:
        noun['gender'] = 'm'

    if noun['type'] in ['de-decl-noun-f', 'de-decl-adj+noun-f']:
        noun['gender'] = 'f'

    if noun['type'] in ['de-decl-noun-n', 'de-decl-adj+noun-n']:
        noun['gender'] = 'n'

    if noun['type'] == 'de-decl-noun-pl':
        noun['gender'] = 'pl'

    if noun['type'] in ['de-decl-noun-n', 'de-decl-noun-m']:
        noun['genitive_singular_ending'] = get_default(conjugation, '1', '')
        noun['singular'] = word
        get_plural('2')
        noun['dative_plural_def_no_n'] = get_bool(conjugation, '3')

    if noun['type'] == 'de-decl-noun-f':
        noun['genitive_singular_ending'] = ''
        noun['singular'] = word
        get_plural('1')
        noun['dative_plural_def_no_n'] = False

    if noun['type'] == 'de-decl-noun-pl':
        noun['plural'] = word
        noun['dative_plural_def_no_n'] = False

    if noun['type'] in ['de-decl-adj+noun-m', 'de-decl-adj+noun-n']:
        noun['adj_lemma'] = get_default(conjugation, '1', '')
        noun['noun_lemma'] = get_default(conjugation, '2', '')
        noun['genitive_singular_ending'] = get_default(conjugation, '3', '')
        get_plural('4')
        get_dative_plural()

    if noun['type'] == 'de-decl-adj+noun-f':
        noun['adj_lemma'] = get_default(conjugation, '1', '')
        noun['noun_lemma'] = get_default(conjugation, '2', '')
        noun['genitive_singular_ending'] = ''
        get_plural('3')
        get_dative_plural()

    if noun['type'] in ['de-decl-noun-m', 'de-decl-noun-f', 'de-decl-noun-n', 'de-decl-noun-pl',
                                 'de-decl-adj+noun-f', 'de-decl-adj+noun-m', 'de-decl-adj+noun-n']:
        NOUNS.insert_ignore(noun, ['word'])

def add_adj(word, conjugation):
    adj = {'word': word, 'type': conjugation['template_name']}

    adj['lemma'] = get_default(conjugation, 'lemma', adj['word'])
    adj['strong_pred'] = get_bool(conjugation, 'strong_pred')

    if adj['type'] == 'de-decl-adj':
        adj['stem'] = get_default(conjugation, '1', '')
        adj['comparative'] = get_default(conjugation, '2', '')
        adj['superlative'] = get_default(conjugation, '3', '')
        if 'pred' in conjugation:
            if conjugation['pred'] != '-':
                adj['pred'] = conjugation['pred']
        else:
            adj['pred'] = adj['word']

    if adj['type'] == 'de-decl-adj-notcomp':
        adj['stem'] = get_default(conjugation, '1', adj['word'])
        if 'pred' in conjugation:
            if conjugation['pred'] != '-':
                adj['pred'] = conjugation['pred']
        else:
            adj['pred'] = adj['word']

    if adj['type'] == 'de-decl-adj-notcomp-nopred':
        adj['stem'] = get_default(conjugation, '1', adj['word'])

    if adj['type'] in ['de-decl-adj', 'de-decl-adj-notcomp', 'de-decl-adj-notcomp-nopred']:
        ADJS.insert_ignore(adj, ['word'])

def word_cb(data):
    if 'conjugation' in data:
        if data['pos'] == 'verb':
            for conjugation in data['conjugation']:
                add_verb(data['word'], conjugation)
        if data['pos'] in ['noun', 'name']:
            for conjugation in data['conjugation']:
                add_noun(data['word'], conjugation)
        if data['pos'] == 'adj':
            for conjugation in data['conjugation']:
                add_adj(data['word'], conjugation)


wk.parse_wiktionary('enwiktionary.xml.bz2', word_cb, languages=['German'])
print("Yay, all parsed")
