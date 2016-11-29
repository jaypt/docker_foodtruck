#!/usr/bin/python2.7

import geojson
import requests
import json

GIST = 'https://api.github.com/gists'

def read_url(url):
    r = requests.get(url)
    return r.json()

def mapper(data, writeToFile='mapped.geojson', key=None):
    geo_type = {"type": "FeatureCollection"}
    info_list = []

    for info in data:
        temp_info = info
        if key:
            temp_info = info[key]
        line = {}
        line['type'] = 'Feature'
        line['properties'] = {
                              'name' : temp_info.get("applicant", ""),
                              "fooditems": temp_info.get('fooditems', ""),
                              "address": temp_info.get("address", ""),
                              "schedule": temp_info.get("schedule", "")
                              }
        line['geometry'] = {
                            'type': 'Point',
                            'coordinates': (
                                            temp_info.get("longitude",""),
                                            temp_info.get("latitude", "")
                                             )
                            }
        if line['geometry']['coordinates'][0] == "0" or\
           line['geometry']['coordinates'][1] == "0":
             continue
        info_list.append(line)
        
    for line in info_list:
        geo_type.setdefault('features', []).append(line)
        
    with open(writeToFile, 'w') as f:
        f.write(geojson.dumps(geo_type))
    
    

def upload_to_gist_github(fileName='mapped.geojson', api=GIST):

    with open(fileName, 'r') as reader:
        content = reader.read()
    
    files = {}
    files[fileName] = {'content' : content}
    
    description = 'uploading gist file through script'
    public = False
    
    json_info = json.dumps(dict(description=description, public=public, files=files)) 
    response = requests.post(api, data=json_info)
    
    
    return response.json()['html_url']
       
    
if __name__ == '__main__':
    '''
    to get url go to :https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat
    then click on export ---> soda api
    '''
    url = 'https://data.sfgov.org/resource/6a9r-agq8.json'
    data = read_url(url)
    mapper(data)