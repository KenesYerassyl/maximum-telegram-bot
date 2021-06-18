import os.path

from db_controller import DBController
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
from os import environ
from credentials import get_creds

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets/readonly']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

credentials = service_account.Credentials.from_service_account_info(get_creds())

service = build('sheets', 'v4', credentials=credentials)

sheet = service.spreadsheets()

db = DBController()

def get_user_info(user_id):
    result = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range='01.06.2021!A2:A').execute()
    values = result.get('values', [])
    needed_row = -1
    for row in range(len(values)):
        if values[row][0] == user_id:
            needed_row = row
            break
    needed_row += 2
    result1 = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range=f'01.06.2021!D{needed_row}:{needed_row}').execute()
    scores = result1.get('values', [])
    return scores[0]
    

def check_user_id(user_id, chat_id):
    result = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range='01.06.2021!A2:A').execute()
    values = result.get('values', [])
    needed_row = -1
    for row in range(len(values)):
        if values[row][0] == user_id:
            needed_row = row
            break
    if needed_row == -1:
        return False
    else:
        does_chat_exist = db.does_chat_exist(chat_id)
        if does_chat_exist == False:
            db.add_subscriber(chat_id, user_id)
        else:
            db.modify_user_id(chat_id, user_id)
        return True
