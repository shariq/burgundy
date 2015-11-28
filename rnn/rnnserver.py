# make sure to drop this file in the char-rnn directory
# creates a pool of words, and adds to the pool when it starts getting too small

import traceback
import remotequeue
import time
import rnn
import pronounce
import random

Q = remotequeue.make('secret', False)
amazing_models = open('amazing_models').read().splitlines()

def sample_model(model, chars = 5000):
    try:
        model_path = model.split(';')[0].strip()
        temp = model.split(';')[1].strip()
        words = rnn.run_temperature(model_path, temp, chars).splitlines()[2:-2]
        print model,'generated',len(words)
        return words
    except:
        print traceback.format_exc()
        return []

def create_words(num):
    print 'creating',num,'words'
    pool = set()
    while len(pool) < num * 1.5:
        model = random.choice(amazing_models)
        print 'sampling from model',model
        for word in sample_model(model):
            if 12 > len(word) > 3:
                if random.random() < len(word)/8:
                    if word[0] == 'c':
                        if random.random() > 0.2:
                            continue
                    if word[0] == 'b':
                        if random.random() > 0.5:
                            continue
                    pool.add(word)
    print 'created that many words! now sorting by pronunciation score...'
    words = sorted(pool, key = pronounce.score)
    return words[-num:]

while True:
    while Q.qsize() < 2500:
        print 'we have only',Q.qsize(),'words'
        words = create_words(250)
        for word in words:
            Q.put(word)
    time.sleep(0.25)


