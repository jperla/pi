from __future__ import with_statement
"""
    Ivy Pi Memorizer
    Copyright 2008 Ivy Call, LLC <contact AT@AT ivycall.com>

    THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND.

    2008-03-13
    Released by Author: Joseph Javier Perla

    LICENSE: GPLv3
"""

import nltk

pronunciations = nltk.corpus.cmudict.transcriptions()
word = 'NINETIETH'

def load_soundmap(filename='sounds.csv'):
    import csv
    soundmap = {}
    with open('sounds.csv', 'r') as f:
        reader = csv.reader(f)
        for sound, map in reader:
            soundmap[sound] = map
    return soundmap

soundmap = load_soundmap('sounds.csv')

def convert_word_to_digits(word):
    word = word.upper()
    try:
        return ''.join(soundmap[syllable] \
                                        for syllable in pronunciations[word][0])
    except KeyError, e:
        raise Exception('Unknown word: %s' % word, e)

def convert_to_digits(phrase):
    return ''.join(convert_word_to_digits(word) for word in phrase.split(' '))



assert(convert_to_digits('NINETIETH') == '2211')
assert(convert_to_digits('FAN') == '82')
assert(convert_to_digits('soap') == '09')
assert(convert_to_digits('fiction') == '8762')
assert(convert_to_digits('minnie mouse') == '3230')
assert(convert_to_digits('paisley') == '905')
assert(convert_to_digits('photo') == '81')
assert(convert_to_digits('mug') == '37')
assert(convert_to_digits('ties') == '10')



