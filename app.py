"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Google Sheets API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/sheets
2. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def send_data(sheet, service, values, spreadsheet_id):
    range_ = "'{0}'!A1".format(sheet)
    value_input_option = 'RAW'  
    insert_data_option = 'OVERWRITE'  
    
    value_range_body = {
        'values': [values]
    }
    print(range_)
    print(values)
    
    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()

if __name__ == '__main__':

    print(tools.argparser)
    try:
        import argparse
        custom_argparser = argparse.ArgumentParser(tools.argparser)
        custom_argparser.add_argument("--spreadsheet_id", type=str, required=True)
        custom_argparser.add_argument("--sheet", type=str, required=True)

        flags = custom_argparser.parse_args()
    except ImportError as e:
        flags = None

    from googleapiclient import discovery
    credentials = get_credentials()
    service = discovery.build('sheets', 'v4', credentials=credentials)
    
    values = [1, 2, 3, 4] 
    
    send_data(flags.sheet, service, values, flags.spreadsheet_id)
