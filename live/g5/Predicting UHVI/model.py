import tensorflow as tf
from shapely.geometry import LineString, Point
import math
import json

LAYER_DIR = 'live/g5/Predicting UHVI'

def call(input_args):

    amenities = input_args['amenities']
    trees = input_args['trees']
    parking_places = input_args['parking_places']

    with open(f'{LAYER_DIR}/data.geojson', 'r') as f:
        data = json.loads(f.read())

    point = Point(input_args['street']['lng'], input_args['street']['lat'])

    distances = []
    for feature in data['features']:
        line = LineString(feature['geometry']['coordinates'])
        point2 = line.interpolate(line.project(point))
        dist = point.distance(point2)
        distances.append(dist)

    idx = distances.index(min(distances))

    closest_feature = data['features'][idx]

    model = tf.keras.models.load_model(f'{LAYER_DIR}/TFmodel_UHI.h5')

    # create input to model
    input_vec = [[
        closest_feature['properties']['length'],
        closest_feature['properties']['amenities'],
        closest_feature['properties']['buildings'],
        closest_feature['properties']['trees'],
        closest_feature['properties']['benches'],
        closest_feature['properties']['fountain'],
        closest_feature['properties']['drinking water'],
        closest_feature['properties']['art pts'],
        closest_feature['properties']['short term parking'],
        closest_feature['properties']['parking_places'],
        closest_feature['properties']['waterinfluence'],
        closest_feature['properties']['grassinfluence'],
        closest_feature['properties']['DIRhori'],
        closest_feature['properties']['GLO_hori_real'],
        closest_feature['properties']['GLO_hori_d'],
        closest_feature['properties']['SSD_sum'],
    ]]

    uhi = model.predict(input_vec)

    closest_feature['properties']['hover'] = f'<span style="font-weight:bold">UHI: </span>{float(uhi[0][0]):.4f}'
    street = [closest_feature]
    return street
