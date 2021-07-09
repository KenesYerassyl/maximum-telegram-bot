import os.path
import socket
import messages

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
attendance_sheet_id = environ.get("ATTENDANCE_SPREADSHEET_ID")
testresults_sheet_id = environ.get("TESTRESULTS_SPREADSHEET_ID")
sheet = service.spreadsheets()