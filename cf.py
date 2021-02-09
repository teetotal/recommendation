import pandas as pd

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

#const
factors = 100
epochs = 20

# Creation of the dataframe. Column names are irrelevant.
df = pd.DataFrame(
    {
        'items': ['1', '1', '1', '2', '2'],
        'users': [9, 32, 2, 45, 'user_foo'],
        'ratings': [3.1, 2.1, 4.4, 3.0, 1.12]
    }
    )

# A reader is still needed but only the rating_scale param is requiered.
reader = Reader(rating_scale=(0, 5))

# The columns must correspond to user id, item id and ratings (in that order).
data = Dataset.load_from_df(df[['users', 'items', 'ratings']], reader)

# Load the movielens-100k dataset (download it if needed),
#data = Dataset.load_builtin('ml-100k')

#trainset, testset = train_test_split(data, test_size=.1)
trainset = data.build_full_trainset()
testset = trainset.build_anti_testset()

# We'll use the famous SVD algorithm.
algo = SVD(n_factors=factors, n_epochs=epochs, verbose=False)

# Train the algorithm on the trainset, and predict ratings for the testset
algo.fit(trainset)
cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
# We can now use this dataset as we please, e.g. calling cross_validate
cross_validate(NormalPredictor(), data, cv=5, verbose=True)

predictions = algo.test(testset, verbose=False)
recommends = get_top_n(predictions)
'''
for recommend in recommends:
    print(recommend, recommends[recommend])
'''
uid = str(2)  # raw user id (as in the ratings file). They are **strings**!
iid = str(2)  # raw item id (as in the ratings file). They are **strings**!

# get a prediction for specific users and items.
#pred = algo.predict(uid, iid, r_ui=4, verbose=True)
algo.predict(uid, '2', verbose=True)
algo.predict(uid, '1', verbose=True)
print(uid, recommends[uid])