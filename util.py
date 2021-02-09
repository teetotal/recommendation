import os
from h5 import h5_read

def get_data(path, is_print = True):
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
def load_data(_path):
    files = read_dir(_path)

    users = []
    items = []
    ratings = []
    
    for f in files:
        u, i, r = get_data(_path + "/" + f)
        
        users.extend(u)
        items.extend(i)
        ratings.extend(r)

    return users, items, ratings

def load_data_cluster(_path):
    h5 = h5_read(_path)
    data = h5['/train']['data'][()]

    aids = []
    ratings = []
    for aid in data:
        aids.append(aid)
        ratings.append(data[aid])

    return aids, ratings

def load_result_cluster(_path):
    h5 = h5_read(_path)
    result = h5['/cluster']['result'][()]
    h5.close()
    return result
    
def get_query(sql_file_path):
    with open(sql_file_path, 'r') as file:
        q = file.read()
    return q    