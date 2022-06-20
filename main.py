from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request, send_from_directory
from random import random
from pathlib import Path
import importlib
import time
import json
import os


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def list_layers(parent):
    """ checks `parent` directory for sub-directories that can be considered a
        layer, i.e. contains 'style.json' and 'geo.geojson'.
    """
    dirs = [x for x in Path(parent).iterdir() if x.is_dir()]
    layers = []
    for d in dirs:
        files = [x.stem for x in list(d.iterdir())]
        if 'style' in files and 'geo' in files:
            layers.append(d.stem)
    return layers

@app.route('/<path:path>/staticlayers', methods=['GET'])
@cross_origin()
def static_layers(path):
    return json.dumps(list_layers(f'static/{path}'))

@app.route('/<path:path>/livelayers', methods=['GET'])
@cross_origin()
def live_layers(path):
    live_layers = {}
    for group in list_layers(f'live/{path}'):
        with open(f'live/{path}/{group}/inputs.json', 'r') as inputs:
            live_layers[group] = json.loads(inputs.read())
    return live_layers

@app.route('/static/<path:path>', methods=['GET'])
@cross_origin()
def static_jsons(path):
    return send_from_directory('static', path)

@app.route('/live/<path:path>', methods=['GET'])
@cross_origin()
def live_jsons(path):
    return send_from_directory('live', path)


@app.route('/api', methods=['POST'])
@cross_origin()
def api():
    input_args = json.loads(request.data)
    model_id = input_args.pop('model')
    group = input_args.pop('group')
    model = importlib.import_module(f'live.{group}.{model_id}.model')

    with open(f'live/{group}/{model_id}/geo.geojson', 'r') as f:
        geojson = json.loads(f.read())
        geojson['features'] = model.call(input_args)

    return jsonify(geojson)

