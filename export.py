from export_util import *
import os
from h5 import *

path_dir = 'data'
if not os.path.exists(path_dir):
    os.makedirs(path_dir)

size_loading_data = 2000000
idx = 0
cnt_file = 0
query = get_query('data.sql')

while True:
    users = []
    items = []
    ratings = []

    q = query + "LIMIT " + str(idx) + ", " + str(size_loading_data)    
    rows = get_data(q)
    if len(rows) == 0:
        break
    print(idx, len(rows))

    for row in rows:
        users.append(str(row[0]).encode('utf8'))
        items.append(str(row[1]).encode('utf8'))
        ratings.append(float(row[2]))

    path = path_dir + '/train-' + str(cnt_file) + '.h5'
    h5 = h5_gen(path, 'gzip')
    h5.write('/train', 'users', users)
    h5.write('/train', 'items', items)
    h5.write('/train', 'ratings', ratings)
    h5.close()

    print(path, len(users), len(items), len(ratings))

    idx += size_loading_data
    cnt_file += 1

print("Done.")