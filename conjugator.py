""" Uses scraped data to conjugate and declenate German verbs, nouns and adjectives """
import dataset

DB = dataset.connect('sqlite:///german.db')
VERBS = DB.get_table('verb')
NOUNS = DB.get_table('noun')
ADJVS = DB.get_table('adjective')

def conjugate_verb(inf):
    """ verb conjugater """
    data = VERBS.find_one(word=inf)

    if not data:
        print("oh no, not found")
        return {}

    conjugations = {'infinitive': inf}

    voices = [
        'first person singular',
        'second person singular informal',
        'third person singular',
        'second person plural',
        'first person plural',
        'second person singular formal'
        ]
    if data['seperable_prefix'] == '':
        seperable_end = ''
    else:
        seperable_end = ' ' + data['seperable_prefix']

    conjugations['present first person singular'] = data['present_stem'] + 'e' + seperable_end
    if data['e_on_present_second_third']:
        e_maybe = 'e'
    else:
        e_maybe = ''
    conjugations['present second person informal'] = data['present_second_third_stem'] + e_maybe + 'st' + seperable_end
    conjugations['present third person'] = data['present_second_third_stem'] + e_maybe + 't' + seperable_end
    conjugations['present second person'] = data['present_stem'] + e_maybe + 'st' + seperable_end
    conjugations['past participle'] = data['past_participle']

    return conjugations

def make_card_noun(noun):
    """ verb conjugater """
    data = NOUNS.find_one(word=noun)

    if not data:
        print("oh no, not found")
        return {}

    card = {}
    if data['type'] == 'de-decl-noun-m':
        card['gender'] = 'm'
    if data['type'] == 'de-decl-noun-f':
        card['gender'] = 'f'
    if data['type'] == 'de-decl-noun-n':
        card['gender'] = 'n'
    if data['type'] == 'de-decl-noun-pl':
        card['gender'] = 'pl'

    if card['gender'] in ['m', 'n', 'f', 'pl']:
        card['nominative_singular'] = noun
        if card['gender'] in ['m', 'n']:
            card['genetive_singular'] = noun + data['genitive_singular_ending']
            if data['genitive_singular_ending'] in ['n', 'en', 'ns', 'ens']:
                card['weak_n'] = True
            else:
                card['weak_n'] = False

        if data['plural'] != None:
            card['plural'] = data['plural']
        elif data['plural_ending'] != None:
            card['plural'] = noun + data['plural_ending']

    return card

CARD = make_card_noun('Junge')
for field in CARD:
    print("{0}: {1}".format(field, CARD[field]))
