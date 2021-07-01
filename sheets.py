import os.path
import json
import socket

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

socket.setdefaulttimeout(600) 
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
        result1 = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range=f'{sheet_name}!A{needed_row}:P{needed_row}').execute()
        user_info = result1.get('values', [])[0]
        result2 = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range=f'{sheet_name}!A1:P1').execute()
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
    if values == None:
        return False
    for row in range(len(values)):
        if values[row] != None and len(values[row]) > 0 and values[row][0] == user_id:
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

def get_all_tests():
    return db.get_all_tests()

# remote -> Google Sheets, local -> MongoDB
def new_sheet_released():
    local_sheets = []
    for item in db.get_all_tests():
        local_sheets.append(item["test_name"])

    remote_sheets = []
    result = service.spreadsheets().get(spreadsheetId=environ.get("SPREADSHEET_ID")).execute()
    for item in result.get('sheets', ''):
        if item["properties"]["title"].startswith("Тест ") == True:
            remote_sheets.append(item["properties"]["title"])

    # Check if local has test which was deleted from remote
    # If has, delete test from local
    for item in local_sheets:
        if item not in remote_sheets:
            db.delete_test(item)

    if len(remote_sheets) == len(local_sheets):
        return None
    else:
        print("Validation 1: New Sheet appeared.")
        new_test_name = None
        for item in remote_sheets:
            if item not in local_sheets:
                new_test_name = item
                break
        if new_test_name == None:
            return None
        else:
            print("Validation 2: Checking if the table is finished!")
            result1 = sheet.values().get(spreadsheetId=environ.get("SPREADSHEET_ID"), range=f'{new_test_name}!Q2:Q2').execute()
            if "values" in result1:
                print("Validation 3: The cell Q2:Q2 has some value")
                if result1.get('values', '')[0][0] == 'TRUE':
                    db.add_test(new_test_name)
                    print("Validation 4: The cell has value 'TRUE'")
                    return new_test_name
                else:
                    return None
            else:
                return None