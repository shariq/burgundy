# this is what I used after training a bunch of models to pick which models to use
# all just very hacky exploratory code
# updated the same script while changing things around; it does multiple things at different sections

import sys
import pdb
import rnn
import re
import shutil
from collections import defaultdict
import os
import pronounce

training_data = open('training_data').read()
burgundy_words = open('burgundy_words.txt').read().splitlines()

def score(s):
    groups = s.split(';')
    scores = []
    for group in groups:
        words = group.splitlines()[:-1]
        scores.append(score_words(words))
    return sum(sorted(scores)[-3:])/15 + 1.0

def clean_some(s):
    groups = s.split(';')
    scores = []
    for group in groups:
        words = group.splitlines()[:-1]
        scores.append((','.join(word for word in words if word), score_words(words)))
    stuffs = map(lambda x:x[0], sorted(scores, key = lambda x:x[1]))
    return '\n'.join(stuffs[-3:][::-1])

def score_words(words):
    output = 0
    seen_already = set()
    bad_words = ['care', 'car', 'caar', 'cara', 'core']
    for word in words:
        if word in seen_already:
            output += -50
        elif len(word) <= 4:
            output += -20*(5-len(word))
        elif len(word) > len('listerine'):
            output += -50
        elif word in bad_words:
            output += -30
        elif word in burgundy_words:
            output += -10
        else:
            output += pronounce.score(word)
        seen_already.add(word)
    if len(words) == 0:
        return -30
    return output/len(words)

def clean(s):
    out = ','.join(x for x in s.splitlines() if x).replace(';','\n')
    out += '\n'
    words = len([x for x in s.splitlines() if x])
    #out += 'score: '+str(score(s))
    return out

model_locations = (m.start() for m in re.finditer('.t7 ;', training_data))

models = defaultdict(lambda: set())

for model_location in model_locations:
    line_begin = training_data.rfind('\n', 0, model_location) + 1
    line_end = training_data.find('\n', model_location)
    model = training_data[line_begin:line_end].split('.t7 ;')[0] + '.t7'
    models[model.strip()].add(line_end + 1)

model_data = {}
model_samples = {}

for model in models:
    model_sample = ''
    for index in models[model]:
        model_sample += training_data[index:index+100].strip() + ';'
    model_samples[model] = model_sample
    model_data[model] = clean(model_sample)

model_data_keys = model_data.keys()



observed_models = open('observed_models').read().split('\n\n')
generators = set()
for observed_model in observed_models:
    model, words = observed_model.strip().splitlines()
    words = words.replace(')','').replace('(','').replace(' ','').split(',')
    for index in models[model]:
        model_sample = training_data[index:index+100]
        for word in words:
            if word in model_sample:
                line_end = index - 1
                line_start = training_data.rfind('\n', 0, line_end - 1)
                generators.add(training_data[line_start+1:line_end].strip())

model_scores = {}

for model_temp in generators:
    model = model_temp.split(';')[0].strip()
    temp = model_temp.split(';')[1].replace(':','').strip()
    words = rnn.run_temperature(model, temp, 1000).splitlines()
    model_scores[model_temp] = score_words(words)

models_score_ordered = map(lambda x:x[0], sorted(model_scores.items(), key = lambda x:x[1]))
models_score_ordered.reverse()

print '\n'.join(models_score_ordered[:5])
sys.exit(0)

#pdb.set_trace()

results = sorted(model_samples.items(), key = lambda x:score(x[1]))
results.reverse()
for result in results:
    print score(result[1])
    print result[0]
    print clean_some(result[1])
    str(raw_input())

sys.exit(0)

good_models = []
bad_models = []

definitely_good_models = []
definitely_bad_models = []

if os.path.exists('good_models'):
    for model in open('good_models').read().splitlines():
        definitely_good_models.append(model)
if os.path.exists('bad_models'):
    for model in open('bad_models').read().splitlines():
        definitely_bad_models.append(model)

i = 0

while i < len(model_data):
    print '\n'
    print i,'of',len(model_data)-len(definitely_good_models)-len(definitely_bad_models)
    model = model_data_keys[i]
    if model in definitely_good_models or model in definitely_bad_models:
        i += 1
        continue
    print model_data[model]
    instruction = str(raw_input('[(skip)/Y(es)/N(o)/B(ack)/D(one)]: ')).lower().strip()
    if len(instruction) > 1:instruction = instruction[0]
    if instruction == 'b':
        i -= 1
        model = model_data_keys[i]
        while model in definitely_good_models or model in definitely_bad_models:
            i -= 1
            model = model_data_keys[i]
        print 'going back'
        continue
    if instruction == 'n':
        if model in good_models:
            good_models.remove(model)
        bad_models.append(model)
        print model,'added to bad models'
    if instruction == 'y':
        if model in bad_models:
            bad_models.remove(model)
        good_models.append(model)
        print model,'added to good models'
    i += 1
    good_model_s = ''
    for model in good_models + definitely_good_models:
        good_model_s += model + '\n'
    bad_model_s = ''
    for model in bad_models + definitely_bad_models:
        bad_model_s += model + '\n'
    if os.path.exists('good_models'):
        shutil.copy('good_models', 'good_models_bkp')
    if os.path.exists('bad_models'):
        shutil.copy('bad_models', 'bad_models_bkp')
    with open('good_models','w') as f:
        f.write(good_model_s)
    with open('bad_models','w') as f:
        f.write(bad_model_s)
    if instruction == 'd':
        break
