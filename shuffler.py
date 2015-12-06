# just a quick hack to improve words in the pool
import remotequeue
import random
import time

Q = remotequeue.get('127.0.0.1', 'secret')
bad_words = set(['molest', 'turdurine', 'amamanus', 'amananus', 'malester', 'molaster', 'malaster', 'maloster'])

while True:
    word_pool = []
    while Q.qsize() > 500:
        word = Q.get()
        if word in word_pool or word in bad_words:
            continue
        word_pool.append(word)
    random.shuffle(word_pool)
    for word in word_pool:
        Q.put(word)
    time.sleep(5)
