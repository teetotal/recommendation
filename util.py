import os
from h5 import h5_read
import numpy as np

def get_cf_data(path, is_print = True):
    h5 = h5_read(path)
    users = h5['/train']['users'][()]
    items = h5['/train']['items'][()]
    ratings = h5['/train']['ratings'][()]
    h5.close()
    
    if is_print == True:
        print("loaded data", path, len(users), len(items), len(ratings))
    
    return users, items, ratings
##################################################################
def read_dir(_path):
    files = os.listdir(_path)
    files = [f for f in files if f.endswith(".h5")]
    files.sort()

    return files
##################################################################
def load_cf_data(_path):
    files = read_dir(_path)

    users = []
    items = []
    ratings = []
    
    for f in files:
        u, i, r = get_cf_data(_path + "/" + f)
        
        for user in u:
            users.append(user.decode('utf8'))
        for item in i:
            items.append(item.decode('utf8'))
        ratings.extend(r)

    return users, items, ratings

def load_data_cluster(_path):
    h5 = h5_read(_path)
    data = h5['/train']

    aids = []
    ratings = []
    for aid in data:
        aids.append(aid)
        ratings.append(np.array(data[aid], np.float))

    h5.close()
    return aids, ratings

def load_result_cluster(_path):
    h5 = h5_read(_path)
    result = h5['/cluster']
    
    ret = []
    for aid in result:
        ret.append([aid, result[aid][0]])

    h5.close()
    return ret
    
def get_query(sql_file_path):
    with open(sql_file_path, 'r') as file:
        q = file.read()
    return q    