import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())
    features = []
    for feature in data['features']:

        hover = feature['properties']['comments']
        feature['properties']['hover'] = hover
        feature['properties'].pop('comments')

        feature['properties']['color'] = feature['properties']['colors']
        feature['properties'].pop('colors')

        feature['properties'].pop('element_type')
        feature['properties'].pop('osmid')

        features.append(feature)

    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

