from export_util import *
from util import *

print("Loading Data")
aids, ratings = load_data_cluster('data_cluster/train.h5')

#const
size_insert = 10000
q = get_query('cluster_import_rating.sql')

while True:
    if len(aids) == 0:
        break
    elif len(aids) < size_insert:
        size_insert = len(aids)

    aids_temp = aids[:size_insert]
    ratings_tmep = ratings[:size_insert]

    aids = aids[size_insert:]
    ratings = ratings[size_insert:]
    
    query = ""
    for n in range(len(aids_temp)):
        row = "('" + aids_temp[n] + "', " 
        for r in ratings_tmep[n]:
            row += str(r) + ','

        query += row[:-1] + "),"
    
    query = query[:-1]
    query = q + query
    execute(query)
    print("Remain", len(aids))

print("Done")