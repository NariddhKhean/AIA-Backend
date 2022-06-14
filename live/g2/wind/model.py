import pandas as pd
import geopandas as gpd
import numpy as np
from shapely import wkt
import requests
import json

def call(input_args):

    ####### load relevant files of preprocessed data #####################################################

    #get normalize wind speed data for edges
    scoredEdges = pd.read_csv('./live/g2/wind/finalScoredEdges.csv') 

    #######################################################################################################

    #get windspeed and direction (using free rapid api account so can't make more than 500 requests a month)

    MY_API_KEY = "4561471e50msh3d1e762ef5340e0p12521djsn5f37f41058cd"

    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    querystring = {"q":"Vienna, Austria","lat":"0","lon":"0","callback":"","id":"2172797","lang":"null","units":"metric"}

    headers = {
        "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
        "X-RapidAPI-Key": "4561471e50msh3d1e762ef5340e0p12521djsn5f37f41058cd"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #convert response to json
    data = json.loads(response.text)

    #parse json for relevent data
    windDirection = data['wind']['deg']
    windSpeed = data['wind']['speed']

    #check which wind column direction to use
    if windDirection > 337.5 and windDirection < 22.5:
        wCol = 'w1'
    elif windDirection > 22.5 and windDirection < 67.5:
        wCol = 'w2'
    elif windDirection > 67.5 and windDirection < 112.5:
        wCol = 'w3'
    elif windDirection > 112.5 and windDirection < 157.5:
        wCol = 'w4'
    elif windDirection > 157.5 and windDirection < 202.5:
        wCol = 'w5'
    elif windDirection > 202.5 and windDirection < 247.5:
        wCol = 'w6'
    elif windDirection > 247.5 and windDirection < 292.5:
        wCol = 'w7'
    else:
        wCol = 'w8'

    windEdges = scoredEdges[['geometry', wCol]]
    windSpeed_list = windEdges[wCol] * windSpeed

    #assign colors
    wColor = []
    for i in range(len(windSpeed_list)):
        if windSpeed_list[i] < 0.5:
            wColor.append('#FFFFF')
        elif windSpeed_list[i] > 0.5 and windSpeed_list[i] <= 1.0 :
            wColor.append('#CFF8FF')
        elif windSpeed_list[i] > 1 and windSpeed_list[i] <= 2 :
            wColor.append('#37DFFF')
        elif windSpeed_list[i] > 2 and windSpeed_list[i] <= 3:
            wColor.append('#22B4CE')
        elif windSpeed_list[i] > 3 and windSpeed_list[i] <= 4:
            wColor.append('#027C93')
        elif windSpeed_list[i] > 4 and windSpeed_list[i] <= 5 :
            wColor.append('#0C505E')
        else: 
            wColor.append('#03323E')

    windEdges[wCol] = windSpeed_list
    windEdges['color'] = wColor

    #convert strings to shapely linestring
    windEdges['geometry'] = windEdges['geometry'].apply(wkt.loads)

    #convert edges to gdf
    windEdges_gdf = gpd.GeoDataFrame(windEdges, crs='EPSG:4326', geometry=windEdges['geometry'])
    windEdges_gdf = windEdges_gdf.dropna()
    wind_geojson = gpd.GeoSeries([windEdges_gdf]).to_json()

    return wind_geojson
