import time
from random import random

def call(input_args):

    print(input_args)

    features = [
        {
            "type": "Feature",
            "properties": {
                "color": "#F7455D",
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    16.3738 + random() / 10 - 0.05,
                    48.2082 + random() / 10 - 0.05,
                    0.0
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "color": "#33C9EB",
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    16.3738 + random() / 10 - 0.05,
                    48.2082 + random() / 10 - 0.05,
                    0.0
                ]
            }
        },
    ]
    return features
