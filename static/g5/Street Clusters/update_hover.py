import json

with open('old.geojson', 'r') as f:
    data = json.loads(f.read())

    for i, feature in enumerate(data['features']):
        props = feature['properties']

        uhvi = props["Urban Heat  Vulnerability Index"]
        if uhvi != 'missing information':
            uhvi = f'{float(uhvi):.4f}'

        wi = props["Water influence"]
        if wi == 'missing information':
            wi = '0.0000'
        if wi != 'missing information':
            wi = f'{float(wi):.4f}'

        gi = props["Grass influence"]
        if gi == 'missing information':
            gi = '0.0000'
        else:
            gi = f'{float(gi):.4f}'

        hover = f"""
            {props["description"]}<br/><br/>
            <span style="font-weight:bold">Street Type: </span>{props["Street type"]}<br/>
            <span style="font-weight:bold">Street Material: </span>{props["Street material"]}<br/>
            <span style="font-weight:bold">Amenity Density: </span>{int(props["Amenity density"])}<br/>
            <span style="font-weight:bold">Trees: </span>{int(props["Trees"])}<br/>
            <span style="font-weight:bold">Benches: </span>{int(props["Benches"])}<br/>
            <span style="font-weight:bold">Fountains: </span>{int(props["Fountains"])}<br/>
            <span style="font-weight:bold">Parking Places: </span>{int(props["Parking places"])}<br/>
            <span style="font-weight:bold">Water Influence: </span>{wi}<br/>
            <span style="font-weight:bold">Grass Influence: </span>{gi}<br/>
            <span style="font-weight:bold">Urban Heat Vulnerability Index: </span>{uhvi}
        """
        data['features'][i]['properties']['hover'] = hover

with open('geo.geojson', 'w') as f:
    json.dump(data, f)

