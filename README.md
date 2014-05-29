POI Clustering
==============
Overview
--------
This application aims finding points of interests in Lyon, France, based on pictures metadata retrieved from Flickr.

Dependencies
------------
To setup dependencies, execute the following command from the python folder:
`sudo pip install -r requirements.txt`

If you get the following error: `clang: error: unknown argument: '-mno-fused-madd'`
Please run the following command: `ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install scikit-learn`

Functionalities
------------
- To start the clustering using MeanShift (density based algorithm), execute `python main.py`
- To display the results, execute `python server.py`, then access `localhost:8080` from your browser. The display may take some time.