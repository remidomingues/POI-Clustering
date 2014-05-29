from collections import Counter

import parser
import plot
from pandas import *
from numpy import array, isfinite
import operator
from sklearn.cluster import MeanShift, estimate_bandwidth

import numpy as np
import pylab as pl
from itertools import cycle

# Jouer avec Google Places

def import_data(filepath):
    print 'Importing data from {}...'.format(filepath)
    df = pandas.read_csv(filepath_or_buffer=filepath)  # Read the file
    df.drop_duplicates()
    df[['hashtags', 'legend']] = df[['hashtags', 'legend']].fillna(value='')
    df['hashtags'] = df['hashtags'].apply(lambda h : h.split(',') if h else [])
    df['legend'] = df['legend'].apply(lambda h : h.replace('\\n', '<br/>'))
    return df

# Compute clustering with MeanShift
def run_meanshift(data):
    print 'Clustering data (Meanshift algorithm)...'
    bandwidth = estimate_bandwidth(data, quantile=0.005, n_samples=None)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, min_bin_freq=30, cluster_all=False)
    ms.fit(data)
    return ms

def plot_meanshift(ms_data, cluster_centers, n_centers_):
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    pl.figure(1)
    pl.clf()

    for k, col in zip(cluster_centers['cluster'], colors):
        cluster_points = ms_data[(ms_data['cluster'] == k)]

        cluster_longitudes = cluster_points['longitude']
        cluster_latitudes = cluster_points['latitude']

        cluster_center = cluster_centers[(cluster_centers['cluster'] == k)]

        pl.plot(cluster_longitudes, cluster_latitudes, col + '.')
        pl.plot(cluster_center['longitude'], cluster_center['latitude'], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=14)

    pl.title('POI clustering (%d estimated clusters)' % n_centers_)
    pl.show()

def export_data(ms_data, clusters_file, cluster_centers, centers_file):
    ms_data['date_taken'] = ['{}/{}/{}_{}:{}'.format(row[1]['day_taken'], row[1]['month_taken'], row[1]['year_taken'], row[1]['hour_taken'], row[1]['minutes_taken'], ) for row in ms_data.iterrows()]
    ms_data[['date_taken']] = ms_data[['date_taken']].astype(str)

    print 'Exporting clusters to {}...'.format(clusters_file)
    ms_data.to_csv(path_or_buf=clusters_file, cols=['longitude', 'latitude', 'hashtags', 'date_taken', 'url', 'cluster'], encoding='utf-8')

    print 'Exporting clusters centers to {}...'.format(centers_file)
    cluster_centers.to_csv(path_or_buf=centers_file, cols=['longitude', 'latitude', 'tags', 'cluster'], encoding='utf-8')

if __name__ == "__main__":
    ms_data = import_data("data/knime_data.csv")
    ms_values = ms_data[['longitude', 'latitude']].values

    meanshift = run_meanshift(data=ms_values)
    ms_data['cluster'] = meanshift.labels_

    ms_data = ms_data.sort(columns='cluster')
    # Removing points which belong to no cluster
    ms_data = ms_data[(ms_data['cluster'] != -1)]

    labels_unique = np.unique(meanshift.labels_).tolist()
    del labels_unique[0]

    # Filtering clusters centers according to data filter
    cluster_centers = DataFrame(meanshift.cluster_centers_, columns=['longitude', 'latitude'])
    cluster_centers['cluster'] = labels_unique

    #Counting tags
    tags_list = []
    for center in cluster_centers.iterrows():
        tags = Counter()
        for point in ms_data[(ms_data['cluster'] == center[1]['cluster'])].iterrows():
            tmp_tags = point[1]['hashtags']
            for tag in tmp_tags:
                tags[tag] += 1

        tags = {key : value for key, value in tags.iteritems() if value >= 10}
        tags_list.append(str(sorted(tags.iteritems(), key=operator.itemgetter(1)).reverse()))

    cluster_centers['tags'] = tags_list
    n_centers_ = len(cluster_centers)



    # Removing clusters which contain less than x points
    for k in range(n_centers_):
        try:
            cluster_points = ms_data[(ms_data['cluster'] == k)]
            if len(cluster_points) < 30:
                ms_data = ms_data[(ms_data['cluster'] != k)]
                cluster_centers = cluster_centers[(cluster_centers['cluster'] != k)]
        except:
            cluster_centers = cluster_centers[(cluster_centers['cluster'] != k)]

    print("> Number of estimated clusters: %d" % n_centers_)


    plot_meanshift(ms_data, cluster_centers, n_centers_)

    export_data(ms_data, "results/points.csv", cluster_centers, "results/centers.csv")
