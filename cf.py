import pandas as pd

from surprise import NormalPredictor, Reader
from surprise import SVD, Dataset, accuracy, dump
from surprise.model_selection import cross_validate, train_test_split
from collections import defaultdict

from util import *

def get_top_n(predictions, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, est in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n
def load_model(path):
    import os
    if os.path.exists(path) == True:
        _, algo = dump.load('model_cf')
        return algo
    return None
def load_train_data():
    #data load
    users, items, ratings = load_cf_data('data')
    print('item list-up')
    item_list = {}
    for i in items:
        if (i in item_list) == False:
            item = int(i)
            item_list[item] = {
                'spid': int(item/10),
                'grade': int(item - (int(item/10) * 10)) 
            }
    item_names = []
    for key in item_list:
        item_names.append(key)

    item_spids = {}
    for key in item_list:
        item_spids[item_list[key]['spid']] = True
    item_spids = [k for k in item_spids]

    items = [int(int(item)/10) for item in items]

    # Creation of the dataframe. Column names are irrelevant.
    df = pd.DataFrame(
        {
            'items': items,
            'users': users,
            'ratings': ratings
        }
        )

    # A reader is still needed but only the rating_scale param is requiered.
    reader = Reader(rating_scale=(0, 5))

    # The columns must correspond to user id, item id and ratings (in that order).
    data = Dataset.load_from_df(df[['users', 'items', 'ratings']], reader)

    # Load the movielens-100k dataset (download it if needed),
    #data = Dataset.load_builtin('ml-100k')

    #trainset, testset = train_test_split(data, test_size=.1)
    print('build trainset')
    trainset = data.build_full_trainset()
    #print('build testset')
    #testset = trainset.build_anti_testset()

    return trainset, item_spids

def export_csv(predictions, path = 'cf_prediction.csv'):
    #csv
    import csv

    with open(path, 'w', newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for pred in predictions:
            w.writerow(pred)

    print('Exported CSV', path, len(predictions))

def prediction(uid, items, min_rating = 0.0):
    predictions = []
    for iid in item_spids:
        pred = algo.predict(uid, iid, verbose=False)
        if pred.est >= min_rating:
            predictions.append([ uid, iid, pred.est ])

    return predictions

#const
factors = 100
epochs = 100

model_path = 'model_cf'

trainset, item_spids = load_train_data()
algo = load_model(model_path)
if algo == None:
    algo = SVD(n_factors=factors, n_epochs=epochs, verbose=True)
    algo.fit(trainset)
    dump.dump(model_path, algo=algo)

uid = '3e31df4a5d1efc1f3e033404'
p = prediction(uid, item_spids, 2.0)
t = get_top_n(p)
for aid in t:
    for pred in t[aid]:
        print(aid, [pred])

export_csv(p)


#cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
# Train the algorithm on the trainset, and predict ratings for the testset


# We can now use this dataset as we please, e.g. calling cross_validate
#cross_validate(NormalPredictor(), data, cv=5, verbose=True)

#predictions = algo.test(testset, verbose=True)
#recommends = get_top_n(predictions)
