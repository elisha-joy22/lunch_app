from googleapiclient.discovery import build 
from google.oauth2 import service_account

import os


SERVICE_ACCOUNT_FILE = 'lunch-app.json'
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")


#google sheets
def export_to_google_sheets(data):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    spreadsheet_id = SPREADSHEET_ID
    range_name = 'Sheet1!A1'  # Update this with the range where you want to write data
    body = {
        'values': data
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


