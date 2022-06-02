import time
from random import random

def call(input_args):

    print(input_args)

    time.sleep(5)  # NOTE: mimicking a long running inference...

    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    16.3738 + random() / 10 - 0.05,
                    48.2082 + random() / 10 - 0.05,
                    0.0
                ]
            }
        }
    ]
    return features
