from export_util import *
from util import *

print("Loading Data")
result = load_result_cluster('cluster_result.h5')

#const
size_insert = 20000
q = get_query('cluster_import.sql')

while True:
    if len(result) == 0:
        break
    elif len(result) < size_insert:
        size_insert = len(result)

    data = result[:size_insert]
    result = result[size_insert:]
    
    query = ""
    for d in data:
        query += "('" + d[0] + "', " + str(d[1]) + "),"
    
    query = query[:-1]
    query = q + query
    execute(query)
    print("Remain", len(result))

print("Done")