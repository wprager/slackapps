from flask import Flask, request
from slackapps import app

import requests

# ---------------------------------------
# ROUTES
# ---------------------------------------
@app.route('/')
def index():
	return 'hello world'

