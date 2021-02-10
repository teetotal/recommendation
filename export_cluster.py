from export_util import *
from util import *
import os
from h5 import *
import numpy as np

path_dir = 'data_cluster'
if not os.path.exists(path_dir):
    os.makedirs(path_dir)

size_loading_data = 20000
idx = 0

query = get_query('data_cluster.sql')

data = {}
while True:
    q = query + "LIMIT " + str(idx) + ", " + str(size_loading_data)    
    rows = select(q)
    if len(rows) == 0:
        break
    print(idx, len(rows))

    for row in rows:
        aid = str(row[0]).encode('utf8')
        position = int(row[1])

        if (aid in data) == False:
            data[aid] = [0] * 28

        data[aid][position] += 1

    idx += size_loading_data

path = path_dir + '/train.h5'
h5 = h5_gen(path, 'gzip')
for k in data:
    arr = np.array(data[k])
    _max = arr.max()
    d = arr / _max
    h5.write('/train', k, d)
h5.close()

print(path)
print("Done.")