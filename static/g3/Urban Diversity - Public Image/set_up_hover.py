import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())

    features = []
    for feature in data['features']:
        hover = f"""
            <span style="font-weight:bold">Name: </span>{feature['properties']['name']}<br/>
            <span style="font-weight:bold">Tree Index: </span>{feature['properties']['tree_index']}<br/>
            <span style="font-weight:bold">Public Toilets: </span>{feature['properties']['public_toilets']}<br/>
            <span style="font-weight:bold">Drinking Fountain: </span>{feature['properties']['drinking_fountain']}
        """

        feature['properties']['hover'] = hover
        features.append(feature)
    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

