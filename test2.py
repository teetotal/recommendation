import pandas as pd

import surprise
from surprise import NormalPredictor
from surprise import Reader
from surprise.model_selection import cross_validate

from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
from collections import defaultdict

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
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


# Load the movielens-100k dataset (download it if needed),
data = Dataset.load_builtin('ml-100k')
uids = defaultdict(list)
items = {}

for d in data.raw_ratings:
    uids[d[0]].append([d[1], d[2]])
    items[d[1]] = True

# sample random trainset and testset
# test set is made of 25% of the ratings.
#trainset, testset = train_test_split(data, test_size=.1)
trainset = data.build_full_trainset()
testset = trainset.build_anti_testset()

factors = 100
epochs = 1000
# We'll use the famous SVD algorithm.
algo = SVD(n_factors=factors, n_epochs=epochs, verbose=False)
# Train the algorithm on the trainset, and predict ratings for the testset
algo.fit(trainset)

print(factors, epochs)
acc = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
'''
predictions = algo.test(testset, verbose=False)
# Then compute RMSE
acc = accuracy.mse(predictions, verbose=False)
'''


uid = str(196)  # raw user id (as in the ratings file). They are **strings**!
iid = str(242)  # raw item id (as in the ratings file). They are **strings**!
iid2 = str(393)
# get a prediction for specific users and items.
#pred = algo.predict(uid, iid, r_ui=4, verbose=True)
algo.predict(uid, iid, r_ui=3.0, verbose=True)
algo.predict(uid, iid2, r_ui=4.0, verbose=True)
print(uid, uids[uid], items[iid2])
'''
'''