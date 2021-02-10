from util import load_data_cluster
import numpy as np
from sklearn.cluster import KMeans
from h5 import *

#const
clusters = 16
max_iter = 3000
print("Loading data")
aids, ratings = load_data_cluster('data_cluster/train.h5')

print("Starting K-means")
km = KMeans(n_clusters=clusters, max_iter=max_iter).fit(ratings)

print("Saving Result")
result_file_path = 'cluster_result.h5'
h5 = h5_gen(result_file_path, 'gzip') 

for n in range(len(km.labels_)):
    aid = aids[n]
    cluster = [int(km.labels_[n])]
    h5.write('/cluster', aid, cluster)
h5.close()
print("All Done.", result_file_path)

