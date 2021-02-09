from export_util import *
from util import *

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

    for d in data:
        query += "('" + data[0].decode('utf8') + "', " + str(data[1]) + "),"
    
    query = query[:-1]
    execute(q)
    print("Remain", len(result))

print("Done")