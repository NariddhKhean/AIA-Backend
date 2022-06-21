import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())
    features = []
    for feature in data['features']:

        hover = feature['properties']['comments']
        hover = f'<span style="font-weight:bold">Number of Bikes: </span>{hover.split(":")[1]}'
        feature['properties']['hover'] = hover
        feature['properties'].pop('comments')

        feature['properties']['color'] = feature['properties']['colors']
        feature['properties'].pop('colors')

        feature['properties'].pop('ID')
        feature['properties'].pop('bicycle_parking_count')

        features.append(feature)

    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

