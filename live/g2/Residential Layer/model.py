import tensorflow as tf
from shapely.geometry import LineString, Point
import joblib
import pandas as pd
import json

LAYER_DIR = 'live/g2/Residential Layer'

def call(input_args):
    point = Point(input_args['building']['lng'], input_args['building']['lat'])
    distances = []

    with open(f'{LAYER_DIR}/residential.geojson', 'r') as f:
        gj = json.loads(f.read())

    for feature in gj['features']:
        poly = LineString(feature['geometry']['coordinates'][0])
        point2 = poly.interpolate(poly.project(point))
        distances.append(point.distance(point2))

    idx = distances.index(min(distances))
    closest_feature = gj['features'][idx]

    area = closest_feature['properties']['area']

    model = tf.keras.models.load_model(f'{LAYER_DIR}/ANN-5Dense.h5')

    scalerX = joblib.load(f'{LAYER_DIR}/ANN_5D_scalerXAtoB.save')
    scalerY = joblib.load(f'{LAYER_DIR}/ANN_5D_scalerYAtoB.save')

    new_data = pd.DataFrame([[
        float(area),
        float(input_args['u_val_walls']),
        float(input_args['u_val_roof']),
        float(input_args['u_val_basement']),
        float(input_args['u_val_glass']),
        float(input_args['g_val_glass'])
    ]])

    scaled_input = scalerX.transform(new_data)

    out = model.predict(scaled_input)
    predictions = scalerY.inverse_transform(out)

    #Flatten predictions list to be readable for hops
    pred_list = predictions.tolist()[0]

    closest_feature['properties']['hover'] = f"""
        <span style="font-weight:bold">Typology: </span>{closest_feature['properties']['building']}<br/>
        <span style="font-weight:bold">Area: </span>{closest_feature['properties']['area']} m2<br/></br/>

        <span style="font-weight:bold">U Values:</span><br/>
        Walls: {closest_feature['properties']['u-value-walls_W/m2K']} W/m2K<br/>
        Roof: {closest_feature['properties']['u-value-roof_W/m2K']} W/m2K<br/>
        Basement: {closest_feature['properties']['u-value-basement_W/m2K']} W/m2K<br/>
        Glass: {closest_feature['properties']['u-value-glass_W/m2K']} W/m2K<br/>
        Glass (g value): {closest_feature['properties']['g-value-glass_W/m2K']} W/m2K<br/><br/>

        <span style="font-weight:bold">Energy use:</span><br/>
        Heating Energy: {closest_feature['properties']['Heating-energy-kWh/m2 a']} kWh/m2<br/>
        Cooling Energy: {closest_feature['properties']['Cooling-energy-kWh/m2 a']} kWh/m2<br/>
        DHW Energy: {closest_feature['properties']['DHW-energy-kWh/m2 a']} kWh/m2<br/>
        Total Energy: {closest_feature['properties']['total-energy-kWh/m2 a']} kWh/m2<br/><br/>

        <span style="font-weight:bold">User U Values:</span><br/>
        Walls: {input_args['u_val_walls']} W/m2K<br/>
        Roof: {input_args['u_val_roof']} W/m2K<br/>
        Basement: {input_args['u_val_basement']} W/m2K<br/>
        Glass: {input_args['u_val_glass']} W/m2K<br/>
        Glass (g value): {input_args['g_val_glass']} W/m2K<br/><br/>

        <span style="font-weight:bold">Predicted Energy use:</span><br/>
        Heating Energy: {float(pred_list[0]):.2f} kWh/m2<br/>
        Cooling Energy: {float(pred_list[1]):.2f} kWh/m2<br/>
        DHW Energy: {float(pred_list[2]):.2f} kWh/m2<br/>
        Total Energy: {float(pred_list[3]):.2f} kWh/m2
    """

    return [closest_feature]

