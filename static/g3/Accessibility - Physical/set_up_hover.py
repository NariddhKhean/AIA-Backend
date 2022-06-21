import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())

    features = []
    for feature in data['features']:
        hover = f"""
            <span style="font-weight:bold">Name: </span>{feature['properties']['name']}<br/>
            <span style="font-weight:bold">Elevators: </span>{feature['properties']['elevators']}<br/>
            <span style="font-weight:bold">Low Sidewalk: </span>{feature['properties']['low_sidewalk']}<br/>
            <span style="font-weight:bold">Sidewalk Width: </span>{feature['properties']['sidewalk_width']}<br/>
            <span style="font-weight:bold">Disabled Parking: </span>{feature['properties']['disabled_parking']}
        """

        feature['properties']['hover'] = hover
        features.append(feature)
    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

