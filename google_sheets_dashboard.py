import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Path to the JSON file containing your OAuth client credentials
CLIENT_SECRET_FILE = 'C:\OrderBlockWebsite\client_secret_291062463602-u0s437gfu4dlno0hr8798s1fju0ahtt7.apps.googleusercontent.com.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
   creds = Credentials.from_authorized_user_file('token.json')
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
   if creds and creds.expired and creds.refresh_token:
       creds.refresh(Request())
   else:
       flow = InstalledAppFlow.from_client_secrets_file(
           CLIENT_SECRET_FILE, SCOPES)
       creds = flow.run_local_server(port=8000)
   # Save the credentials for the next run
   with open('token.json', 'w') as token:
       token.write(creds.to_json())

# Use creds to create a client to interact with the Google Sheets API
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1ZtWa2gPxK-t7qITh4O5QXhS5ZtM9xR4IDn6zm4TxNbw'
RANGE_NAME = 'Export!A:J'

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                           range=RANGE_NAME).execute()
values = result.get('values', [])

if not values:
   print('No data found.')
else:
   print('Name, Major:')
   for row in values:
       # Print columns A and B, which correspond to indices 0 and 1.
       print(f'{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}')
