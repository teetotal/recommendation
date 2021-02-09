from util import load_data_cluster
import numpy as np
from sklearn.cluster import KMeans
from h5 import *

#const
clusters = 16
max_iter = 300

aids, ratings = load_data_cluster('data_cluster')
rating = np.array(ratings, np.float)
print("Starting K-means")
km = KMeans(n_clusters=clusters, max_iter=max_iter).fit(ratings)
print("Done K-means")

print("Saving Result")
result = []
for n in range(len(km.labels_)):
    result.append([aids[n], km.labels_[n]])

result_file_path = 'cluster_result.h5'
h5 = h5_gen(result_file_path, 'gzip')    
h5.write('/cluster', 'result', result)
h5.close()
print("All Done.", result_file_path)

