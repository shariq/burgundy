from multiprocessing.managers import BaseManager
from multiprocessing import Queue
import random

PORT = 8989

def get(ip, authkey):
    ''' gets a remote queue on another ip '''
    class RManager(BaseManager):
        ''' manager which connects to a remote queue '''
        pass
    RManager.register('getQueue')
    current_manager = RManager(address=(ip,PORT), authkey=authkey)
    current_manager.connect()
    return current_manager.getQueue()

def make(authkey, public=True):
    ''' makes a remote queue and returns it '''
    class QManager(BaseManager):
        ''' manager of a remote queue '''
        pass
    queue = Queue()
    QManager.register('getQueue', callable=lambda:queue)
    ip = '0.0.0.0' if public else 'localhost'
    qm = QManager(address=(ip, PORT), authkey=authkey)
    qm.start()
    tokens = [random.choice('abcde') for x in range(14)]
    random_token = 'x'.join(tokens)
    globals()['raNdDOmHAkkC82492'] = qm
    return queue

