from elasticsearch import Elasticsearch, exceptions
import time
from flask import Flask, jsonify, request, render_template, redirect
import sys
import requests
from geomapper import *

es = Elasticsearch(host='es', port=9200)
URL = 'https://data.sfgov.org/resource/6a9r-agq8.json'
ES_INDEX = 'sfdata'

app = Flask(__name__)


@app.route('/')
def index():
    msg_all = '''to see map of all food trucks:type 
    <url>/search'''
    eg_all = 'http://localhost:5000/search?food=all'
    msg_query = '''to query specific food: type
    <url>/search?food=<query>'''
    eg_food = 'http://localhost:5000/search?food=chicken' 
    return render_template('index.html', 
                           msg_all=msg_all.split('\n'), 
                           eg_all=eg_all,
                           msg_query=msg_query.split('\n'),
                           eg_food=eg_food)
    


@app.route('/search')
def search():
    key = request.args.get('food', 'all')
    if not key:
        return jsonify({
            "status": "failure",
            "msg": "Please provide a query"
        })
    try:

        max_size = es.count()['count'] 
        if key == 'all':
            res = es.search(index= ES_INDEX, size=max_size)
        else:
            res = es.search(index= ES_INDEX, q=key, size=max_size)
        file = key +'.geojson'
        
        mapper(res['hits']['hits'], writeToFile=file, key='_source')
        
        gist_url = upload_to_gist_github(fileName=file)
        print gist_url
        return render_template('search.html', url=gist_url+'.js')
       
    except Exception as e:
        return jsonify({
            "status": "failure",
            "msg": "error in reaching elasticsearch",

        })
    

def load_data_in_es(url, index, doc_type='truck'):
    """ creates an index in elasticsearch """
    data = read_url(url)
    print "Loading data in elasticsearch ..."
    for id, truck in enumerate(data):
        res = es.index(index=index, doc_type=doc_type, id=id, body=truck)
    print "Total trucks loaded: ", len(data)

def safe_check_index(index, retry=5):
    """ connect to ES with retry """
    if not retry:
        print "Out of retries. Bailing out..."
        sys.exit(1)
    try:
        status = es.indices.exists(index)
        return status
    except exceptions.ConnectionError as e:
        print "Unable to connect to ES. Retrying in 5 secs..."
        time.sleep(5)
        safe_check_index(index, retry-1)


def check_and_load_index(index=ES_INDEX, url=URL):
    """ checks if index exits and loads the data accordingly """
    if not safe_check_index(index):
        load_data_in_es(url, index)




if __name__ == "__main__":
    print "starting flask"
    check_and_load_index()
    app.run(host='localhost', port=5001, debug=True) 
