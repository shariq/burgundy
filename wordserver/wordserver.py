from bottle import route, hook, response, run, request
import datetime
import remotequeue
import sys

Q = remotequeue.get('127.0.0.1', 'secret')

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/')
def index():
    print '[' + str(datetime.datetime.now()) + '] ' + str(request.environ.get('REMOTE_ADDR'))
    sys.stdout.flush()
    return Q.get()

run(host = '0.0.0.0', port = 8080, server = 'tornado')
