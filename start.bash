#!/bin/bash

# build the flask container
docker build -t jaypt/start_flask .

# create the network
docker network create sffdata 

# start the ES container
docker run -d --net sffdata -p 9200:9200 -p 9300:9300 --name es elasticsearch

# start the flask app container
docker run -d --net sffdata -p 5000:5000 --name start_flask jaypt/start_flask

