'''
needs to be located in the same directory as
https://github.com/karpathy/char-rnn
follow instructions in the repo
'''

import hashlib
import os
import random
from subprocess import check_output
import traceback

def unique(obj):
    ''' hashes arbitrarily nested default python types '''
    # this code is so beautiful :'(
    # take a moment to appreciate
    consistent_random_string = 'QsmaHglRfz1hvGPbr4R3UCTDs'
    # string which will never appear in practice; generated randomly
    # set this to '' if integers are equal to their str conversion
    if type(obj) == str:
        return hashlib.md5(obj).hexdigest()
    elif type(obj) == int:
        return unique(consistent_random_string + str(obj))
    elif type(obj) == list or type(obj) == tuple:
        # treats tuples and lists the same
        return unique(str(map(unique, obj)))
    elif type(obj) == dict:
        return unique(sorted(obj.items(), key = lambda x: x[0]))
    elif type(obj) == set:
        # distinguishes between sets and list(sets)
        return unique(consistent_random_string + unique(sorted(list(obj))))
    else:
        return NotImplemented

def train(options = {}):
    cv_directory = unique(options)
    options_list = ['th', 'train.lua', '-data_dir', 'data/words']
    for arg, value in options.items():
        options_list.append('-'+arg)
        options_list.append(str(value))
    options_list.append('-checkpoint_dir')
    options_list.append(cv_directory)
    check_output(options_list)

def run(options = {}):
    cv_directory = unique(options)
    output = ''
    for model in os.listdir():
        for temperature in ['0.05', '0.2', '0.4', '0.6', '0.8', '1.0']:
            if '.t7' not in model:
                continue
                model_path = os.path.join(cv_directory, model)
                options_list = ['th', 'sample.lua', model_path, '-temperature', temperature, '-length', '200']
                current_output = check_output(options_list)
                output += model_path+' ; '+temperature+' :'+'\n'
                output += current_output[-100:].rsplit('\n', 1)[0]
                output += '\n\n'
    return output

def exists(options):
    return os.path.exists(unique(options))

def forever():
    all_options = {
        'rnn_size': [64, 128],
        'num_layers': [2, 3],
        'model': ['lstm', 'gru', 'rnn'],
        'learning_rate': ['2e-3', '2e-6', '2e-1'],
        'dropout': ['0', '0.3', '0.8'],
        'seq_length': map(str, range(2, 8)),
        'batch_size': [1, 3, 5, 10, 20],
        'train_frac': ['0.95', '0.99']
    }
    while True:
        options = {}
        for k, l in all_options.items():
            options[k] = random.choice(l)
        if exists(options):
            continue
        try:
            print '!!!!!'
            print str(options)
            train(options)
            output = run(options)
            print output
            print '!!!!!'
        except:
            print '@@@@@'
            traceback.print_exc()
            print '@@@@@'

if __name__ == '__main__':
    forever()
