import re, datetime, dateutil.parser
datetime = datetime.datetime
from collections import defaultdict

open('timestamps','w').write('\n'.join(map(str, map(lambda td: (((td-datetime(1970,1,1)).microseconds + ((td-datetime(1970,1,1))).seconds + (td-datetime(1970,1,1)).days * 86400) * 10**6) / 10**6,map(dateutil.parser.parse, re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', open('nohup.out').read()))))))

timestamps = map(int, open('timestamps').read().splitlines())

start = min(timestamps)
end = max(timestamps)

seconds = defaultdict(lambda:0)
minutes = defaultdict(lambda:0)
hours = defaultdict(lambda:0)

for timestamp in timestamps:
    seconds[(timestamp-start)] += 1
    minutes[(timestamp-start)/60] += 1
    hours[(timestamp-start)/3600] += 1

to_stringy = lambda x: '\n'.join(map(lambda u:str(u[1]), sorted(x.items(), key = lambda y:y[0])))

open('seconds','w').write(to_stringy(seconds))
open('minutes','w').write(to_stringy(minutes))
open('hours','w').write(to_stringy(hours))
