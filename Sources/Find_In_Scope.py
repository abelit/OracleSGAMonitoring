import subprocess
import re
from collections import defaultdict

search = 140184310124547
process = '8037'
data = subprocess.check_output(['pmap', process])

regex = re.compile('shmid=(\w+)\s')
shmids = [eval('int({0})'.format(x)) for x in regex.findall(data)]

filename = '/proc/{0}/maps'.format(process)

data = defaultdict(list)

with open(filename) as f:
    for line in f:
        line = line.split()
        _id = int(line[4])
        if _id not in shmids:
            continue
        data[_id].append(line[0].split('-'))

for k, v in data.iteritems():
    for x in v:
        if search in xrange(long(x[0], 16), long(x[1], 16)):
            print k