from bottle import route, hook, response, run
from threading import Thread
import random
import time

words = set()

def update():
    while True:
        try:
            with open('words.txt') as f:
                for word in f.read().splitlines():
                    words.add(word)
        except:
            pass
        time.sleep(15)

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/')
def index():
    return random.choice(tuple(words))

t = Thread(target = update)
t.daemon = True
t.start()

run(host = '0.0.0.0', port = 8080, server = 'tornado')
