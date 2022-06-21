import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())

    features = []
    for feature in data['features']:
        hover = f"""
            <span style="font-weight:bold">Diversity Index: </span>{feature['properties']['diversity_index']:.4f}<br/><br/>

            <span style="font-weight:bold">Afro_Ratio: </span>{feature['properties']['afro_ratio']}<br/>
            <span style="font-weight:bold">Asian_Ratio: </span>{feature['properties']['asian_ratio']}<br/>
            <span style="font-weight:bold">Mid_East_Ratio: </span>{feature['properties']['mid_east_ratio']}<br/>
            <span style="font-weight:bold">South_Asian_Ratio: </span>{feature['properties']['south_asian_ratio']}<br/>
            <span style="font-weight:bold">Latinx_Ratio: </span>{feature['properties']['latinx_ratio']}<br/>
            <span style="font-weight:bold">European_Ratio: </span>{feature['properties']['european_ratio']}
        """

        feature['properties']['hover'] = hover
        features.append(feature)
    data['features'] = features

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

