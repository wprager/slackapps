from flask import Flask, request
from slackapps import app, fireside

import requests

# ---------------------------------------
# ROUTES
# ---------------------------------------
@app.route('/')
def route_index():
	return 'hello world'

@app.route('/fireside', methods=['POST'])
def route_fireside():
	return fireside.fireside(request)
