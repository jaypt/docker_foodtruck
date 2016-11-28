#!/usr/bin/python2.7

import geojson
import requests

def read_url(url):
    r = requests.get(url)
    return r.json()

def mapper(data, writeToFile='mapped.geojson'):
    geo_type = {"type": "FeatureCollection"}
    info_list = []
    
    for info in data:
        line = {}
        line['type'] = 'Feature'
        line['properties'] = {
                              'name' : info.get("applicant", ""),
                              "fooditems": info.get('fooditems', ""),
                              "address": info.get("address", ""),
                              "schedule": info.get("schedule", "")
                              }
        line['geometry'] = {
                            'type': 'Point',
                            'coordinates': (
                                            info.get("longitude",""),
                                            info.get("latitude", "")
                                             )
                            }
        if line['geometry']['coordinates'][0] == "" or\
           line['geometry']['coordinates'][1] == "":
             print line['properties']['name']
        info_list.append(line)
        
    for line in info_list:
        geo_type.setdefault('features', []).append(line)
        
    with open(writeToFile, 'w') as f:
        f.write(geojson.dumps(geo_type))
    
if __name__ == '__main__':
    '''
    to get url go to :https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat
    then click on export ---> soda api
    '''
    url = 'https://data.sfgov.org/resource/6a9r-agq8.json'
    data = read_url(url)
    mapper(data)