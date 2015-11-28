# https://news.ycombinator.com/item?id=4668241
# markov chain scoring based on 20k most common english words

import requests
from collections import Counter
from math import log

corpus = open('20k.txt').read().lower()
# https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt

def trans(w, n):
    return ((w[i:i+n], w[i+n]) for i in range(len(w)-n))

tokens_1 = Counter(t for t,l in trans(corpus, 1))
transitions_1 = Counter(trans(corpus, 1))
tokens_2 = Counter(t for t,l in trans(corpus, 2))
transitions_2 = Counter(trans(corpus, 2))

def score(w):
    score_1 = sum(log(transitions_1[t,l]+1)-log(tokens_1[t]+26) for t,l in trans(w, 1))/len(w)
    score_2 = sum(log(transitions_2[t,l]+1)-log(tokens_2[t]+26**2) for t,l in trans(w, 2))/len(w)
    return score_1 + score_2
