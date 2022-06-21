import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())

    features = []
    for feature in data['features']:
        hover = f'''
            <span style="font-weight:bold">Wind Av: </span>{feature['properties']['windAv']}
        '''
        feature['properties']['hover'] = hover
        features.append(feature)
    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

