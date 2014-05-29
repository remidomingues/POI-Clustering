diff --git a/Projet/python/main.py b/Projet/python/main.py
index 7a712cd..ecf590d 100644
--- a/Projet/python/main.py
+++ b/Projet/python/main.py
@@ -4,10 +4,21 @@ from pandas import *
 from numpy import array
 
 from sklearn.cluster import MeanShift, estimate_bandwidth
+from sklearn.datasets.samples_generator import make_blobs
 
-import numpy as np
-import pylab as pl
-from itertools import cycle
+def test():
+    #Data
+    centers = [[1, 1], [-1, -1], [1, -1]]
+    X, _ = make_blobs(n_samples=10000, centers=centers, cluster_std=0.6)
+
+    # Compute clustering with MeanShift
+    # Parameters: data, quantile=radius max of the cluster, n_samples=minimum points per cluster
+    bandwidth = estimate_bandwidth(X, quantile=0.92, n_samples=1000)
+
+    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
+    ms.fit(X)
+
+    plot.draw_meanshift(X, ms)
 
 
 def run_meanshift(data):
@@ -22,45 +33,7 @@ if __name__ == "__main__":
     #test()
 
     df = pandas.read_csv(filepath_or_buffer="data.csv")  # Read the file
-    ms_data = df[['longitude', 'latitude']]
-    ms_values = ms_data.values
-
-    meanshift = run_meanshift(data=ms_values)
-    #plot.draw_meanshift(data=ms_data, meanshift=ms)
-
-
-
-
-    ms_data['cluster'] = meanshift.labels_
-    ms_data = ms_data.sort(columns='cluster')
-
-    cluster_centers = meanshift.cluster_centers_
-    labels_unique = np.unique(meanshift.labels_)
-
-    n_centers_ = len(cluster_centers)
-    n_clusters_ = len(labels_unique)
-
-    print("Number of estimated clusters: %d" % n_clusters_)
-
-    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
-    pl.figure(1)
-    pl.clf()
-
-    for k, col in zip(range(n_clusters_), colors):
-        if k != -1 and k < n_centers_:
-            cluster_points = ms_data[(ms_data.cluster == k)]
-
-            print len(cluster_points)
-
-            if len(cluster_points) > 30:
-                cluster_longitudes = cluster_points['longitude']
-                cluster_latitudes = cluster_points['latitude']
-        
-                cluster_center = cluster_centers[k]
-
-                pl.plot(cluster_longitudes, cluster_latitudes, col + '.')
-                pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
-                    markeredgecolor='k', markersize=14)
+    ms_data = df[['longitude', 'latitude']].values
 
-    pl.title('POI clustering (%d estimated clusters)' % n_clusters_)
-    pl.show()
+    ms = run_meanshift(data=ms_data)
+    plot.draw_meanshift(data=ms_data, meanshift=ms)
