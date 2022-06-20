import pandas as pd
import joblib
import pickle
import json
from shapely.geometry import Point
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.kernel_ridge import KernelRidge

LAYER_DIR = 'live/g4/AirBnBEffect'

def call(input_args):
    lat = float(input_args['userPoint']['lat'])
    lon = float(input_args['userPoint']['lng'])
    listing = int(input_args['listing'])
    sqm = float(input_args['sqm'])

    data = pd.read_csv(f'{LAYER_DIR}/ann_final.csv')
    X = data.loc[:,'latitude':'PerSqm']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled)
    y = data.iloc[:,4].to_numpy()
    y = y.reshape(-1, 1)

    scalerY = MinMaxScaler()
    Y_scaled = scalerY.fit_transform(y)
    Y_scaled_df = pd.DataFrame(Y_scaled)

    X_train, X_test, y_train, y_test, data_train, data_test = train_test_split(X_scaled, Y_scaled, data, test_size = 0.2, random_state = 42)

    model = KernelRidge(kernel = "polynomial", degree = 6)
    model.fit(X_train, y_train)

    filename = f'{LAYER_DIR}/test.sav'
    pickle.dump(model, open(filename, 'wb'))

    scalerX_filename = f'{LAYER_DIR}/scalerXAtoB.save'
    joblib.dump(scaler, scalerX_filename)

    scalerY_filename = f'{LAYER_DIR}/scalerYAtoB.save'
    joblib.dump(scalerY, scalerY_filename)

    data_test.info()

    path = f'{LAYER_DIR}/test.sav'

    model = pickle.load(open(path, 'rb'))

    scalerX = joblib.load(f'{LAYER_DIR}/scalerXAtoB.save')
    scalerY = joblib.load(f'{LAYER_DIR}/scalerYAtoB.save')

    new_data = pd.DataFrame([[lat,lon,listing,sqm]])
    scaled_input = scalerX.transform(new_data)
    out = model.predict(scaled_input)
    predictions = scalerY.inverse_transform(out)
    pred_list = predictions.tolist()
    flat_list = []

    for i in pred_list:
        flat_list += i
    deviation = int(flat_list[0])

    center = Point([lat, lon])
    poly = list(center.buffer(0.00325).exterior.coords)
    poly = [[p[1], p[0]] for p in poly]
    adjusted_poly = []
    for x, y in poly:
        y = lat + (lat - y) / 1.48
        adjusted_poly.append([x, y])

    return [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [adjusted_poly]
            },
            "properties": {
                "hover": f'<span style="font-weight:bold">Deviation: </span>{deviation}%'
            }
        }
    ]

