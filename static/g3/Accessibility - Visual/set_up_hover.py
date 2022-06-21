import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())

    features = []
    for feature in data['features']:
        hover = f"""
            <span style="font-weight:bold">Name: </span>{feature['properties']['name']}<br/>
            <span style="font-weight:bold">Acoustic Lights: </span>{feature['properties']['acoustic_lights']}<br/>
            <span style="font-weight:bold">Tactile Sidewalks: </span>{feature['properties']['tactile_sidewalks']}<br/>
            <span style="font-weight:bold">Low Sidewalks: </span>{feature['properties']['low_sidewalk']}
        """

        feature['properties']['hover'] = hover
        features.append(feature)
    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

