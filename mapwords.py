from __future__ import with_statement
"""
    Ivy Pi Memorizer
    Copyright 2008 Ivy Call, LLC <contact AT@AT ivycall.com>

    THIS SOFTWARE IS SUPPLIED WITHOUT WARRANTY OF ANY KIND.

    2008-03-13
    Released by Author: Joseph Javier Perla

    LICENSE: GPLv3
"""

import csv
import collections

import nltk

import soundmap

with open('nouns.csv', 'r') as f:
    reader = csv.reader(f)
    words = {}
    for word in reader:
        words[word[0].lower()] = soundmap.convert_to_digits(word[0])

word_soundmap = {}
for word in words:
    digits = words[word]
    if digits in word_soundmap:
        word_soundmap[digits].append(word)
    else:
        word_soundmap[digits] = [word]

pi = '''14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912983367336244065664308602139494639522473719070217986094370277'''

def longest_word(digits):
    #most number of consonant sounds in a word is 10
    for i in range(max(len(digits), 10), 0, -1):
        subdigits = digits[0:i]
        if subdigits in word_soundmap:
            return word_soundmap[subdigits], subdigits


def map_words(nums):
    if len(nums) == 0:
        return []
    else:
        word, digits = longest_word(nums)
        remaining = nums[len(digits):]
        words = [word]
        words.extend(map_words(remaining))
        return words


def load_frequencies(filename='word_frequencies.txt'):
    """
    rows = [line.split('\t') for line in open(filename, 'r').readlines()]
    frequencies = {}
    for row in rows:
        frequencies[row[1].lower()] = int(row[3].strip('\n\r '))
    return frequencies
    """
    frequencies = collections.defaultdict(int)
    words = [w.lower() for w in nltk.corpus.gutenberg.words()]
    for word in words:
        frequencies[word] += 1
    return dict(frequencies)

frequencies = load_frequencies()

def get_best_word(choice):
    f = [frequencies.get(word, 0) for word in choice]
    return choice[f.index(max(f))]

def get_best_mapping(nums):
    choices = map_words(nums)
    words = []
    for choice in choices:
        unused = list(set(choice) - set(words))
        if len(unused) > 0:
            words.append(get_best_word(unused))
        else:
            words.append(get_best_word(choice))
    return words
