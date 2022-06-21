import json

with open('Apartments_ GeoJson.geojson', 'r') as f:
    data = json.loads(f.read())

    features = []
    for feature in data['features']:
        if feature['geometry']['type'] == 'Polygon':

            if feature['properties']['Heating-energy-kWh/m2 a'] != None and \
                    feature['properties']['Cooling-energy-kWh/m2 a'] != None and \
                    feature['properties']['DHW-energy-kWh/m2 a'] != None and \
                    feature['properties']['total-energy-kWh/m2 a'] != None and \
                    feature['properties']['u-value-walls_W/m2K'] != None and \
                    feature['properties']['u-value-roof_W/m2K'] != None and \
                    feature['properties']['u-value-basement_W/m2K'] != None and \
                    feature['properties']['u-value-glass_W/m2K'] != None and \
                    feature['properties']['g-value-glass_W/m2K'] != None:

                # hover = f"""
                #     <span style="font-weight:bold">Typology: </span>{feature['properties']['building']}<br/>
                #     <span style="font-weight:bold">Area: </span>{feature['properties']['area']} m2<br/></br/>

                #     <span style="font-weight:bold">U Values:</span><br/>
                #     Walls: {feature['properties']['u-value-walls_W/m2K']} W/m2K<br/>
                #     Roof: {feature['properties']['u-value-roof_W/m2K']} W/m2K<br/>
                #     Basement: {feature['properties']['u-value-basement_W/m2K']} W/m2K<br/>
                #     Glass: {feature['properties']['u-value-glass_W/m2K']} W/m2K<br/>
                #     Glass (g value): {feature['properties']['g-value-glass_W/m2K']} W/m2K<br/><br/>

                #     <span style="font-weight:bold">Energy use:</span><br/>
                #     Heating Energy: {feature['properties']['Heating-energy-kWh/m2 a']} kWh/m2<br/>
                #     Cooling Energy: {feature['properties']['Cooling-energy-kWh/m2 a']} kWh/m2<br/>
                #     DHW Energy: {feature['properties']['DHW-energy-kWh/m2 a']} kWh/m2<br/>
                #     Total Energy: {feature['properties']['total-energy-kWh/m2 a']} kWh/m2
                # """
                # feature['properties']['hover'] = hover

                features.append(feature)
    data['features'] = features

with open('apartments.geojson', 'w') as f:
    json.dump(data, f)

