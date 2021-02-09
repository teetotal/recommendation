from export_util import *
import os
from h5 import *

size_loading_data = 100000
idx = 0
query = get_query('data.sql')

users = []
items = []
ratings = []

while True:
    q = query + "LIMIT " + str(idx) + ", " + str(size_loading_data)    
    rows = get_data(q)
    if len(rows) == 0:
        break
    print(idx, len(rows))

    for row in rows:
        users.append(row[0])
        items.append(str(row[1]))
        ratings.append(float(row[2]))

    idx += size_loading_data

path_dir = 'data'
if not os.path.exists(path_dir):
    os.makedirs(path_dir)

path = path_dir + '/train.h5'
h5 = h5_gen(path, 'gzip')
h5.write('/train', 'users', users)
h5.write('/train', 'items', items)
h5.write('/train', 'ratings', ratings)

print("Done.", path, len(users), len(items), len(ratings))
