"""
    Ivy Pi Memorizer
    Copyright 2008 Ivy Call, LLC <contact AT@AT ivycall.com>

    THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND.

    2008-03-13
    Released by Author: Joseph Javier Perla

    LICENSE: GPLv3
"""
import nltk

def grab_leaves(tree):
    if len(tree[nltk.wordnet.HYPONYM]) == 0:
        return tree.words
    else:
        leaves = []
        for hyponym in tree[nltk.wordnet.HYPONYM]:
            leaves.extend(grab_leaves(hyponym))
        return leaves

def get_all_physical_entities():
    physical_entity = nltk.wordnet.N['physical_entity'].synsets()[0]
    return grab_leaves(physical_entity)

def endswith_any(word, endings):
    return any(True for ending in endings if word.endswith(ending))


abstract_noun_endings = ['ness','tion','ly','day','aire','berg','ing','ant','ry','ity', 'ese', 'lpn']

all_verbs = set(nltk.wordnet.V.keys())
all_adjectives = set(nltk.wordnet.ADJ.keys())
all_adverbs = set(nltk.wordnet.ADV.keys())
all_non_nouns = all_verbs.union(all_adjectives).union(all_adverbs)
physical_entities = set([w.lower() for w in get_all_physical_entities()])
pronounce_words = set([w.lower() for w in nltk.corpus.cmudict.transcriptions()])
gutenberg_words = set([w.lower() for w in nltk.corpus.gutenberg.words()])
dictionary_words = set([w.lower() for w in nltk.corpus.words.words()])
bad_words = set(['nigger','cunnilingus','fetish','vagina'])
manual_abstract_nouns = set(['life','amaranth','jacob','backup','changer','woof','ounce','baker','phoebe','geneva','fennel','digs','anise','savoy','outtake','osage','epicure','gneiss','nisei','packer','footage','soave','jonah','klutz','minium','swatch','gean','gene','jenny','johnny','jane','fed','backer','haft','shawnee','fission','novice','cob','neve','heifer','chino'])
normal_words = pronounce_words - bad_words - manual_abstract_nouns

common_nouns = physical_entities.intersection(normal_words) - all_non_nouns
concrete_nouns = [noun for noun in common_nouns \
                            if not endswith_any(noun, abstract_noun_endings) \
                                and len(noun) >= 3]



import csv
w = csv.writer(open('nouns.csv', 'w'))
for noun in concrete_nouns:
    w.writerow([noun.replace('_', ' ')])

