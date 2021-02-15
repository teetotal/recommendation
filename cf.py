from cf_util import *

from surprise import NormalPredictor, Reader
from surprise import SVD, Dataset, accuracy, dump
from surprise.model_selection import cross_validate, train_test_split
from collections import defaultdict

import argparse

def get_top_n(predictions, n=10):
    top_n = defaultdict(list)
    for uid, iid, est in predictions:
        top_n[uid].append((iid, est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n



def export_csv(predictions, path = 'cf_prediction.csv'):
    #csv
    import csv
    print('exporting csv...')
    with open(path, 'w', newline='') as csvfile:
        w = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for pred in predictions:
            w.writerow(pred)

    print('Exported CSV', path, len(predictions))

def prediction(aids, items, min_rating = 0.0, user_item = None):
    print('Predicting... users', len(aids), 'items', len(items))
    predictions = []

    total_aid = len(aids)
    cnt_aid = 0
    for aid in aids:
        cnt = 0
        for iid in items:
            if user_item == None or (iid in user_item[aid]) == False:
                pred = algo.predict(aid, iid, verbose=False)
                if pred.est >= min_rating:
                    predictions.append([ aid, iid, pred.est ])
                    cnt += 1
        cnt_aid += 1
        if cnt_aid % 100 == 0:
            print(str(cnt_aid) + '/' + str(total_aid), 'appended', aid, cnt)

    return predictions


parser = argparse.ArgumentParser()
parser.add_argument('--factors', type=int, required=False, default=100, help="default 100.")
parser.add_argument('--epochs', type=int, required=False, default=100, help="default 100.")
parser.add_argument('--model', type=str, required=False, default='model.cf', help="default model.cf.")
parser.add_argument('--refit', type=int, required=False, default=0, help="0 <= false, 0 > true default 0.")
parser.add_argument('--user', type=str, required=False, default='3e31df4a5d1efc1f3e033404', help="specify user to recommend. default None. 3e31df4a5d1efc1f3e033404")
parser.add_argument('--csv', type=int, required=False, default=1, help="0 <= false, 0 > true default 1.")
args = parser.parse_args()
factors = args.factors
epochs = args.epochs
model_path = args.model
if args.user == None:
    user = None
else:
    user = [args.user]

if args.refit <= 0: refit = False
else: refit = True

if args.csv <= 0: is_csv = False
else: is_csv = True

print('params', args)

trainset, aids, spids, user_item = load_train_data()
algo = load_model(model_path)

is_create_model = False
if algo == None:
    algo = SVD(n_factors=factors, n_epochs=epochs, verbose=True)
    is_create_model = True

if is_create_model == True or refit == True:
    algo.fit(trainset)
    dump.dump(model_path, algo=algo)

    print('Testing...')
    print('\tbuild testset')
    #accuracy
    testset = trainset.build_testset()
    print('\ttesting')
    predictions = algo.test(testset, verbose=False)
    print('\tget rmse')
    # RMSE should be low as we are biased
    rmse = accuracy.rmse(predictions, verbose=True)

#uid = '3e31df4a5d1efc1f3e033404'
if user == None:
    user = aids
else:
    print('check accuracy')
    u = user_item[user[0]]
    for i in u:
        print(i, u[i])
        algo.predict(user[0], i, verbose=True )

p = prediction(user, spids, 2.0, user_item)
t = get_top_n(p)
for aid in t:
    for pred in t[aid]:
        print(aid, [pred])

if is_csv == True:
    export_csv(p)


#cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
# Train the algorithm on the trainset, and predict ratings for the testset


# We can now use this dataset as we please, e.g. calling cross_validate
#cross_validate(NormalPredictor(), data, cv=5, verbose=True)

#predictions = algo.test(testset, verbose=True)
#recommends = get_top_n(predictions)
