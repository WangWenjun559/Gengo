#!/usr/bin/python
# 
# nltk_helper.py
# 
# General helper util functions
# 
# Note: 
# Some code was borrowed since the naive nltk tokenizer wasn't perfect.
# http://stackoverflow.com/questions/14095971/how-to-tweak-the-nltk-sentence-tokenizer

import nltk
import nltk.data
import codecs
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
# from nltk.corpus import wordnet
from nltk.stem import porter, snowball

def parse_file_to_sentences(filename):
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'ms', 'mrs', 'prof', 'inc', 'no', 'e.g', 'i.e'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    fp = open(filename, "r")
    data = fp.read()
    data = data.replace('?"', '? "').replace('!"', '! "').replace('."', '. "')

    sentences = []
    for para in data.split('\n'):
        if para:
            sentences.extend(sentence_splitter.tokenize(para))
    return sentences

def parse_text_to_sentences(text):
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'ms', 'mrs', 'prof', 'inc', 'no', 'e.g', 'i.e'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    data = text
    data = data.replace('?"', '? "').replace('!"', '! "').replace('."', '. "')

    sentences = []
    for para in data.split('\n'):
        if para:
            sentences.extend(sentence_splitter.tokenize(para))
    return sentences

# def getSynonyms(word):
#     syns = wordnet.synsets(word)
#     #To get rid of duplicates, we first convert to set.
#     synonyms = list(set([l.name.replace('_', ' ') for s in syns for l in s.lemmas]))
#     return synonyms

# def areSynonyms(word1, word2):
#     return word2 in getSynonyms(word1)

# def printSynonyms(word):
#     print getSynonyms(word)

# Stemmer based on Porter Stemmer.
# TODO: Maybe look into snowball stemmer? Tried to do this, but unicode conflicts.
def get_stem(word):
    stemmer = porter.PorterStemmer()
    return stemmer.stem(word)

def has_same_stem(word1, word2):
    return get_stem(word1) == get_stem(word2)

# Splits sentence to clauses separated by commas or semicolons
def split_sentence(sentence):
    minSentLen = 6 

    splitList = [",", ";"]
    wordList = nltk.word_tokenize(sentence)

    wCount = 0
    wordBuf = ""
    finalList = []
    for i in xrange(len(wordList)): 
        tok = wordList[i]
        if i == len(wordList) - 1:
            wCount += 1
            if (wCount < minSentLen):
                if len(finalList) == 0: 
                    finalList.append(wordBuf)
                else:
                    finalList.append(finalList.pop() + tok + " " + wordBuf)
            else: 
                finalList.append(wordBuf)
        elif tok in splitList:
            if (wCount < minSentLen):
                if len(finalList) == 0: 
                    finalList.append(wordBuf)
                else:
                    finalList.append(finalList.pop() + tok + " " + wordBuf)
            else:
                finalList.append(wordBuf) 
            wCount = 0
            wordBuf = ""
        else:
            wordBuf = tok if wordBuf == "" else wordBuf + " " + tok
            wCount += 1

    return finalList

if __name__ == '__main__':
    testList = [
"When I am feeling down and want to eat, \
I like to eat apple sauce, banana splits, and Herman Zhuice.",
"Just as English itself has borrowed words \
from many different languages over its history, \
English loanwords now appear in many languages around the world, \
indicative of the technological and cultural influence of its speakers.",
"It was nominated for ten Academy Awards and won five, \
including Best Picture, Best Director for Hazanavicius, \
and Best Actor for Dujardin, who was the first French \
actor ever to win for Best Actor."
    ]
    for sent in testList:
        print splitSentence(sent)

