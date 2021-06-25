from enum import unique
from dotenv import load_dotenv
from os import environ, read
from pymongo import MongoClient
import pymongo

load_dotenv()
# NOTE: MongoDB -> Cluster(MongoDB Client) -> Database(Set of collections) -> Collection(Table) -> Documents(Row)

class DBManager:

    def __init__(self) -> None:
        user_password = environ.get("DB_USER_PASSWORD")
        self.client = MongoClient(f"mongodb+srv://kenesyearssyl-admin:{user_password}@maximum-telegram-bot.zi7ov.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client.maximum_telegram_bot_db
        
        self.subscriptions = self.db.subscriptions
        self.subscriptions.create_index([('chat_id', pymongo.ASCENDING)], unique=True)

        self.tests = self.db.tests
        self.tests.create_index('test_name', unique=True)
    
    def get_all_users(self):
        try:
            result = self.subscriptions.find({"status" : True})
            return result
        except Exception as e:
            print(f"Finding document failed: {e}")
            return []

    def does_chat_exist(self, chat_id):
        try:
            result = self.subscriptions.find_one({"chat_id" : chat_id})
            return -1 if result == None else result["user_id"]
        except Exception as e:
            print(f"Finding document failed: {e}")
            return -1

    def add_subscriber(self, chat_id, user_id, status=True):
        document = {
            "chat_id" : chat_id,
            "user_id" : user_id,
            "status" : status
        }
        try:
            self.subscriptions.insert_one(document)
        except Exception as e:
            print(f"Inserting document into collection failed: {e}")
    
    def modify_user(self, chat_id, user_id, status=True):
        try:
            self.subscriptions.update_one({"chat_id" : chat_id}, {"$set" : {"user_id" : user_id, "status" : status}})
        except Exception as e:
            print(f"Modifying user id failed: {e}")

    def modify_status(self, chat_id, status):
        try:
            self.subscriptions.update_one({"chat_id" : chat_id}, {"$set" : {"status" : status}})
        except Exception as e:
            print(f"Modifying status failed: {e}")

    def add_test(self, test_name):
        document = {
            "test_name" : test_name
        }
        try:
            self.tests.insert_one(document)
        except Exception as e:
            print(f"Inserting document into collection failed: {e}")

    def delete_test(self, test_name):
        try:
            self.tests.delete_one({"x" : test_name})
        except Exception as e:
            print(f"Deleting document into collection failed: {e}")

    def get_all_tests(self):
        try:
            result = self.tests.find()
            return result
        except Exception as e:
            print(f"Finding document failed: {e}")
            return []