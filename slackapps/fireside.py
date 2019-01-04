from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import datetime
import requests

def fireside(form_text, form_url):
	""" Takes the text and response_url from the slack POST request, and submits a fireside chat question to the google sheet of responses.
		Args:
			form_text (str): the question being submitted
			form_url (str): the slack response_url to later post the delayed responses
		Returns:
			str: a message indicating success
	"""
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
	SPREADSHEET_ID = '1LsMxR7Q1mQ6B2cT8KLaMAO6vjRxyUGJDobL1KntcD1U'
	COL_RANGE = 'Form Responses 1!A1:C1'
	
	# handle blank/help cases
	if form_text == '':
		return 'Please enter a question.'
	if form_text == 'help':
		return 'Usage: /fireside <your question here>\n Example: /fireside What is your name?'
	
	# create request body
	timestamp = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
	properties = {}
	properties['values'] = []
	properties['values'].append([timestamp, form_text])
	
	# get oauth credentials and authorize
	store = file.Storage('token.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('slackapps/util/google_sheets_client_secrets.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))
	
	# make post request to google sheets api
	result = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=COL_RANGE, valueInputOption='RAW', body=properties).execute()
	
	# send delayed response after google api call
	if form_url:
		data = {
			'response_type': 'in_channel',
			'text': 'Question successfully submitted. See you at the next session!'
		}
		requests.post(form_url, json=data)
