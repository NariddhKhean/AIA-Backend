import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())

    features = []
    for feature in data['features']:
        hover = f"""
            <span style="font-weight:bold">Roman Catholic: </span>{feature['properties']['rom-cath']}<br/>
            <span style="font-weight:bold">Evangelical: </span>{feature['properties']['evang']}<br/>
            <span style="font-weight:bold">Jew: </span>{feature['properties']['jew']}<br/>
            <span style="font-weight:bold">Islam: </span>{feature['properties']['islam']}<br/>
            <span style="font-weight:bold">Orthodox: </span>{feature['properties']['ortho']}<br/>
            <span style="font-weight:bold">Other: </span>{feature['properties']['other']}<br/>
            <span style="font-weight:bold">Without: </span>{feature['properties']['without']}
        """

        feature['properties']['hover'] = hover
        features.append(feature)
    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

