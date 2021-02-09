import os
from h5 import h5_read

def get_data(path, is_print = True):
    h5 = h5_read(path)
    users = h5['/train']['users'][()]
    items = h5['/train']['items'][()]
    ratings = h5['/train']['ratings'][()]
    
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