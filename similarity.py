import os
import io
from surprise import KNNBaseline
from surprise import Dataset
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a， %d %b %Y %H:%M:%S')


# Training recommendation model steps: 1
def getSimModle(data):
    # Default loading of movielens dataset
    
    trainset = data.build_full_trainset()
    #Using pearson_baseline method to calculate similarity False calculates similarity between movies based on item
    sim_options = {'name': 'pearson_baseline', 'user_based': False}
    ##Using KNNBaseline algorithm
    algo = KNNBaseline(sim_options=sim_options)
    #Training model
    algo.fit(trainset)
    return algo


# Getting id to name mapping steps: 2
def read_item_names():
    """
    //Get the mapping of movie name to movie id and movie id to movie name
    """
    file_name = (os.path.expanduser('~') +
                 '/.surprise_data/ml-100k/ml-100k/u.item')
    rid_to_name = {}
    name_to_rid = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]
    return rid_to_name, name_to_rid


# Recommendation steps for related movies based on the previous training model:3
def showSimilarMovies(algo, rid_to_name, name_to_rid):
    # Get raw_id of the movie Toy Story (1995)
    toy_story_raw_id = name_to_rid['Toy Story (1995)']
    print('raw_id=' + toy_story_raw_id)
    #Converting raw_id of a movie to the internal ID of the model
    toy_story_inner_id = algo.trainset.to_inner_iid(toy_story_raw_id)
    print('inner_id=' + str(toy_story_inner_id))
    #Get Recommended Movies from Model Here are 10
    toy_story_neighbors = algo.get_neighbors(toy_story_inner_id, 10)
    print('neighbors_ids=' + str(toy_story_neighbors))
    #The internal id of the model is converted to the actual movie id
    neighbors_raw_ids = [algo.trainset.to_raw_iid(inner_id) for inner_id in toy_story_neighbors]
    #Get a movie id list or a movie recommendation list
    neighbors_movies = [rid_to_name[raw_id] for raw_id in neighbors_raw_ids]
    print('The 10 nearest neighbors of Toy Story are:')
    for movie in neighbors_movies:
        print(movie)


data = Dataset.load_builtin('ml-100k')
uids = defaultdict(list)
items = {}

for d in data.raw_ratings:
    uids[d[0]].append([d[1], d[2]])
    items[d[1]] = True

# Get the mapping of id to name
rid_to_name, name_to_rid = read_item_names()

# Training Recommendation Model
algo = getSimModle(data)

##Display related movies
showSimilarMovies(algo, rid_to_name, name_to_rid)

uid = str(196)  # raw user id (as in the ratings file). They are **strings**!
iid = str(242)  # raw item id (as in the ratings file). They are **strings**!
iid2 = str(393)
# get a prediction for specific users and items.
#pred = algo.predict(uid, iid, r_ui=4, verbose=True)
algo.predict(uid, iid, r_ui=3.0 , verbose=True)
algo.predict(uid, iid2, verbose=True)
print(uid, uids[uid], items[iid2])