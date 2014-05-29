from flask import Flask, render_template, request
import json
import pandas
import math
import random

app = Flask(__name__)
app.debug = True

filepathPoints = "./results/points.csv"
filepathClusters = "./results/centers.csv"


def max_cluster(list_points, key):
    max_c = 0
    for p in list_points : 
        distance =math.sqrt(math.pow( p[0]-key[0],2) + (math.pow(p[1]- key[1],2) ))
        if distance > max_c :
            max_c = distance
            return p
    return 0


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/mapPoint", methods = ['POST','GET'])
def generatePoints():
    if request.method == 'GET':
        points = pandas.read_csv(filepath_or_buffer=filepathPoints)  # Read the file

        table_points = points[['longitude', 'latitude','hashtags','url' ,'cluster' ]]
        table_points = table_points.fillna('').values.tolist()

        points = pandas.read_csv(filepath_or_buffer=filepathClusters)  # Read the file
        table_clusters = points[['longitude','latitude','cluster', 'tags']].fillna('').values.tolist()


        # now creating a list of objects in this form : [cluster_number, center point] , [list of the points contained in this cluster]
        result =[ [ [cluster,[clust for clust in table_clusters if clust[2] == cluster][0],10 ], [l for l in table_points if l[4] == cluster]  ] for cluster in set([ p[4] for p in table_points])]
        
        for cluster in result :
            for point in cluster[1] :
                point[1] = point[1]+0.0005-(random.randint(0,10)/10000.0)#max_cluster(cluster[1],cluster[0][1])
                point[0] = point[0]+0.0005-(random.randint(0,10)/10000.0)#max_cluster(cluster[1],cluster[0][1])

        return json.dumps(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
