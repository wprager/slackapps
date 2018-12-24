from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import requests

def fireside(request):
	""" Takes a post request and submits a fireside chat question to the google sheet of responses.
		Args:
			request (Request): the post request; the 'text' parameter should contain the question being submitted
		Returns:
			str: a message indicating success
	"""
	SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
	SPREADSHEET_ID = '1LsMxR7Q1mQ6B2cT8KLaMAO6vjRxyUGJDobL1KntcD1U'
	COL_RANGE = 'Form Responses 1!A1:B1'
	
	# get oauth credentials and authorize
	store = file.Storage('token.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('slackapps/util/google_sheets_client_secrets.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))
	
	# get 'text' param and create request body
	question = str(request.form['text'])
	properties = {}
	properties['values'] = []
	properties['values'].append([question])
	
	# make post request to google sheets api
	result = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=COL_RANGE, valueInputOption='RAW', body=properties).execute()
	
	return 'Question successfully submitted. See you at the next session!'
