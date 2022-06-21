import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())

    features = []
    for feature in data['features']:
        hover = f"""
            <span style="font-weight:bold">Total Men: </span>{feature['properties']['tot_men']}<br/>
            <span style="font-weight:bold">Total Women: </span>{feature['properties']['tot_wom']}<br/><br/>

            <span style="font-weight:bold">Total Austrian Ratio: </span>{feature['properties']['tot_aus_ratio']}<br/>
            <span style="font-weight:bold">Total Foreign Ratio: </span>{feature['properties']['tot_foreign_ratio']}<br/></br/>

            <span style="font-weight:bold">Density: </span>{feature['properties']['density']}
        """

        feature['properties']['hover'] = hover
        features.append(feature)
    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

