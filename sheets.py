import os.path
import json

from db_controller import DBManager
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

db = DBManager()

def get_user_info(user_id, sheet_name):
    result = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range=f'{sheet_name}!A2:A').execute()
    values = result.get('values', [])
    needed_row = -1
    for row in range(len(values)):
        if values[row][0] == user_id:
            needed_row = row
            break
    if needed_row == -1:
        return None
    else:
        needed_row += 2
        result1 = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range=f'{sheet_name}!A{needed_row}:O{needed_row}').execute()
        user_info = result1.get('values', [])[0]
        result2 = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range=f'{sheet_name}!A1:O1').execute()
        info_names = result2.get('values', [])[0]

        response = {}
        for index in range(len(user_info)):
            response[info_names[index]] = user_info[index]
        return response

def does_chat_exist(chat_id):
    return  db.does_chat_exist(chat_id)

def get_user_id(chat_id):
    return db.get_user_id(chat_id)

def unsubscribe_user(chat_id):
    db.modify_status(chat_id, False)

def check_user_id(user_id, chat_id):
    result = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range='Ученики!A2:A').execute()
    values = result.get('values', [])
    needed_row = -1
    for row in range(len(values)):
        if values[row][0] == user_id:
            needed_row = row
            break
    if needed_row == -1:
        return False
    else:
        if does_chat_exist(chat_id) == -1:
            db.add_subscriber(chat_id, user_id)
        else:
            db.modify_user(chat_id, user_id)
        return True

def get_all_users():
    return db.get_all_users()

def new_sheet_released():
    with open("sheets.json", "r") as read_file:
        local_sheets = json.load(read_file).get("sheets")
    sheet_amount = len(local_sheets)

    result = service.spreadsheets().get(spreadsheetId=environ.get("SPREADSHEET_ID")).execute()
    remote_sheets = result.get('sheets', '')
    if len(remote_sheets) == sheet_amount:
        return False
    else:
        found = False
        for item in remote_sheets:
            if item["properties"]["title"] == f"Тест {sheet_amount + 1}":
                found = True
                break
        if found == False:
            return False
        else:
            result1 = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range=f'Тест {sheet_amount + 1}!P2:P2').execute()
            if "values" in result1:
                return result1.get('values', '')[0][0] == 'TRUE'
            else:
                return False
