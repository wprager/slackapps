from flask import Flask, request, Response
from slackapps import app, fireside

import json
import requests

# ---------------------------------------
# ROUTES
# ---------------------------------------
@app.route('/')
def route_index():
	return 'hello world'

@app.route('/fireside', methods=['POST'])
def route_fireside():
	data = {
		'response_type': 'in_channel',
		'text': fireside.fireside(request)
	}
	return Response(json.dumps(data), status=200, mimetype='application/json')
