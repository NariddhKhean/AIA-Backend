import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())

    features = []
    for feature in data['features']:
        if feature['properties']['percentage_density'] == '':
            feature['properties']['percentage_density'] = 0.0
        else:
            feature['properties']['percentage_density'] = float(feature['properties']['percentage_density'])
        features.append(feature)

    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

