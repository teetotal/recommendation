import pandas as pd
from surprise import *
from util import *

def distinct(arr):
    obj = {}
    for e in arr:
        if (e in obj) == False:
            obj[e] = True

    arr = [k for k in obj]

    return arr

def load_model(path):
    import os
    if os.path.exists(path) == True:
        _, algo = dump.load(path)
        print('loaded model', path)
        return algo
    
    print('not exists model', path)
    return None

def load_train_data():
    print('Load data')
    users, items, ratings = load_cf_data('data')
    '''
    print('\tdistinct items')
    item_list = {}
    spids = []
    for i in items:
        if (i in item_list) == False:
            item = int(i)
            item_list[item] = {
                'spid': int(item/10),
                'grade': int(item - (int(item/10) * 10)) 
            }
            spids.append(int(item/10))
    '''
    print('\tdistinct users')
    aids = distinct(users)
    
    print('\tredefine items')
    items = [int(item) for item in items]

    print('\tdistinct items')
    spids = distinct(items)
    
    print('\tlist-up user-item')
    user_item = {}
    for n in range(len(users)):
        if (users[n] in user_item) == False:
            user_item[users[n]] = {}
        if items[n] in user_item[users[n]]:
            print('conflict', users[n], items[n])
        
        user_item[users[n]][items[n]] = ratings[n]

    print('\tcreation of the dataframe.')
    df = pd.DataFrame(
        {
            'items': items,
            'users': users,
            'ratings': ratings
        }
        )
    print('\ttrasforming to df')
    # A reader is still needed but only the rating_scale param is requiered.
    reader = Reader(rating_scale=(0, 5))

    # The columns must correspond to user id, item id and ratings (in that order).
    data = Dataset.load_from_df(df[['users', 'items', 'ratings']], reader)

    # Load the movielens-100k dataset (download it if needed),
    #data = Dataset.load_builtin('ml-100k')

    #trainset, testset = train_test_split(data, test_size=.1)
    print('\tbuild trainset')
    trainset = data.build_full_trainset()
    #print('build testset')
    #testset = trainset.build_anti_testset()

    return trainset, aids, spids, user_item