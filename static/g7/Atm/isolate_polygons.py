import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())
    features = []
    for feature in data['features']:

        hover = feature['properties']['comments']
        hover = f'<span style="font-weight:bold">Number of ATMs: </span>{hover.split(":")[1]}'
        feature['properties']['hover'] = hover
        feature['properties'].pop('comments')

        feature['properties']['color'] = feature['properties']['colors']
        feature['properties'].pop('colors')

        feature['properties'].pop('ID')
        feature['properties'].pop('atm_count')

        features.append(feature)

    data['features'] = features

    print(data)

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

