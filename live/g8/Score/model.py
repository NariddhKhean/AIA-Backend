from math import cos, asin, sqrt
from colorutils import Color
from shapely.geometry import Point
import json

def call(input_args):

    #Open GEOJSON
    with open('live/g8/Score/gameOFgreenGJSON.geojson', 'r') as f:
        gj = json.loads(f.read())

    #New point scored by User
    new_point = []

    number_new_trees = int(input_args['number_new_trees'])
    radius_circle = int(input_args['radius_circle'])

    #Lat and Long from the point selected by User
    lat = input_args['userPoint']['lat']
    lng = input_args['userPoint']['lng']

    # find which point is closest to user
    lat_user = 16.29420959
    lng_user = 48.188331023

    latitudes = []
    longitudes = []

    dictionary=[]
    for i in range(824957):
        dic = {}
        latte = gj['features'][i]['properties']['lat']
        dic['lat'] = latte
        longtte = gj['features'][i]['properties']['lng']
        dic['lon'] = longtte
        dictionary.append(dic)

    def distance(lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        return 12742 * asin(sqrt(hav))

    def closest(data, v):
        return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))

    tempDataList = dictionary

    v = {'lat': lat_user, 'lon': lng_user}

    def list_duplicates_of(seq,item):
        start_at = -1
        locs = []
        while True:
            try:
                loc = seq.index(item,start_at+1)
            except ValueError:
                break
            else:
                locs.append(loc)
                start_at = loc
        return locs

    source = tempDataList
    point_id = int(list_duplicates_of(source, closest(tempDataList, v))[0])

    #score for each year from the point selected by User

    score2001 = gj['features'][point_id]['properties']['score_2001']
    score2002 = gj['features'][point_id]['properties']['score_2002']
    score2003 = gj['features'][point_id]['properties']['score_2003']
    score2004 = gj['features'][point_id]['properties']['score_2004']
    score2005 = gj['features'][point_id]['properties']['score_2005']
    score2006 = gj['features'][point_id]['properties']['score_2006']
    score2007 = gj['features'][point_id]['properties']['score_2007']
    score2008 = gj['features'][point_id]['properties']['score_2008']
    score2009 = gj['features'][point_id]['properties']['score_2009']
    score2010 = gj['features'][point_id]['properties']['score_2010']
    score2011 = gj['features'][point_id]['properties']['score_2011']
    score2012 = gj['features'][point_id]['properties']['score_2012']
    score2013 = gj['features'][point_id]['properties']['score_2013']
    score2014 = gj['features'][point_id]['properties']['score_2014']
    score2015 = gj['features'][point_id]['properties']['score_2015']
    score2016 = gj['features'][point_id]['properties']['score_2016']
    score2017 = gj['features'][point_id]['properties']['score_2017']
    score2018 = gj['features'][point_id]['properties']['score_2018']
    score2019 = gj['features'][point_id]['properties']['score_2019']

    score2020 = gj['features'][point_id]['properties']['score_2020']

    new_tree_distances = ((number_new_trees*radius_circle) / number_new_trees)


    try:
        if new_tree_distances <= 5:
            new_score_2020 = 1 + score2020
    except:
        pass
    try:
        if new_tree_distances > 5 and new_tree_distances <= 10:
            new_score_2020 = 0.8 + score2020
    except:
        pass
    try: 
        if new_tree_distances > 10 and new_tree_distances <= 20:
            new_score_2020 = 0.6 + score2020
    except:
        pass
    try:
        if new_tree_distances > 20 and new_tree_distances <= 35:
            new_score_2020 = 0.4 + score2020
    except:
        pass
    try:
        if new_tree_distances > 35 and new_tree_distances <= 90:
            new_score_2020 = 0.2 + score2020
    except:
        new_score_2020 = score2020

    # list 20 years score from the point selected
    list_20_years_score = [score2001,score2002,score2003,score2004,score2005,
                           score2006,score2007,score2008,score2009,score2010,
                           score2011,score2012,score2013,score2014,score2015,
                           score2016,score2017,score2018,score2019,new_score_2020]

    #Coef. Linear Regreassion Model
    coef_model = [0.00069954,-0.000271,0.00680505,0.00350223,0.01339399,
                  0.01206329,0.02435626, 0.02154593, 0.04283208, 0.03363087, 
                  0.03007545, 0.05138728,0.04665394, 0.05387783, 0.08424082, 
                  0.08033359, 0.08898264, 0.11307264,0.09898938, 0.12179241]

    #Score point selected
    result = []
    for num1, num2 in zip(list_20_years_score, coef_model):
        result.append(num1 * num2)

    score_result = sum(result)

    # colour
    color_score = max(min(score_result, 0.0), 10.0) / 10.0
    c = Color(hsv=(120 * color_score, 1, 1))

    # circle
    center = Point([lat, lng])
    rad = 0.0000065 * radius_circle * 2
    poly = list(center.buffer(rad).exterior.coords)
    poly = [[p[1], p[0]] for p in poly]
    adjusted_poly = []
    for x, y in poly:
        y = lat + (lat - y) / 1.48
        adjusted_poly.append([x, y])

    # hover
    hover = f'<span style="font-weight:bold">Previous Score: </span>{score2020:.2f} / 10<br/><span style="font-weight:bold">New Score: </span>{score_result:.2f} / 10'

    # Here, use the results variable to impact your output
    element = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [adjusted_poly]
        },
        "properties": {
            "color": c.hex,
            "hover": hover
        }
    }

    new_point.append(element)

    return new_point
