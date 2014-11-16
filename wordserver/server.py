from bottle import route, hook, response, run
import random

words = tuple(set(map(lambda x:x.lower().strip(), open('words.txt').read().splitlines())))

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/')
def index():
    return random.choice(words)

run(host = '0.0.0.0', port = 8080, server = 'tornado')
