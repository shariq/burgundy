from bottle import route, hook, response, run
import remotequeue

Q = remotequeue.get('127.0.0.1', 'secret')

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/')
def index():
    return Q.get()

run(host = '0.0.0.0', port = 8080, server = 'tornado')
