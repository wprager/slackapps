from flask import request, Response
from slackapps import app, fireside

import json
import threading

# ---------------------------------------
# ROUTES
# ---------------------------------------
@app.route('/')
def route_index():
	return 'hello world'

@app.route('/fireside', methods=['POST'])
def route_fireside():
	form_text = str(request.form['text'])
	form_url = str(request.form['response_url'])
	
	data = {
		'response_type': 'in_channel',
		'text': 'Submitting question...'
	}
	
	t = threading.Thread(target=fireside.fireside, args=(form_text, form_url,))
	t.start()
	
	return Response(json.dumps(data), status=200, mimetype='application/json')
