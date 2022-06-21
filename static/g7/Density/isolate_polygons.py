import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())
    features = []
    for feature in data['features']:

        feature['properties']['color'] = feature['properties']['colors']
        feature['properties'].pop('colors')

        feature['properties'].pop('popden12')

        features.append(feature)

    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

