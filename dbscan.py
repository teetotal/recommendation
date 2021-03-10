from util import load_data_cluster
import numpy as np
from sklearn.cluster import DBSCAN
from h5 import *

#const. default로 설정
eps = 0.5
min_samples = 5


print("Loading data")
aids, ratings = load_data_cluster('data_cluster/train.h5')

print("Starting DBSCAN")
dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(ratings) 

print("Saving Result")
result_file_path = 'dbscan_result.h5'
h5 = h5_gen(result_file_path, 'gzip') 

for n in range(len(dbscan.labels_)):
    aid = aids[n]
    cluster = [int(dbscan.labels_[n])]
    h5.write('/cluster', aid, cluster)
h5.close()
print("All Done.", result_file_path)

