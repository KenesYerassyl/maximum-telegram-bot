import sqlite3

class DBController:

    def __init__(self, database_file) -> None:
        self.connection = sqlite3.connect(database_file)

    def does_chat_exist(self, chat_id):
        try:
            with self.connection:
                result = self.connection.execute("SELECT * FROM subscriptions WHERE chat_id=?", (str(chat_id),)).fetchall()
            response = -1 if len(result) == 0 else result[0]
            if response == -1:
                return -1
            else:
                return response[1]
        except Exception as e:
            print(f"Error in DB: {e}")
            return -1

    def add_subscriber(self, chat_id, user_id, status = True):
        try:
            with self.connection:
                self.connection.execute("INSERT INTO subscriptions (chat_id, user_id, status) VALUES (?, ?, ?)", (str(chat_id), user_id, status))
        except Exception as e:
            print(f"Error in DB: {e}")

    def modify_status(self, chat_id, status):
        try:
            with self.connection:
                self.connection.execute("UPDATE subscriptions SET status=? WHERE chat_id=?", (status, str(chat_id)))
        except Exception as e:
            print(f"Error in DB: {e}")

    def modify_user_id(self, chat_id, user_id):
        try:
            with self.connection:
                self.connection.execute("UPDATE subscriptions SET user_id=? WHERE chat_id=?", (user_id, str(chat_id)))
        except Exception as e:
            print(f"Error in DB: {e}")
    
    def delete_chat(self, chat_id):
        try:
            with self.connection:
                self.connection.execute("DELETE FROM subscriptions WHERE chat_id=?", (str(chat_id),))
        except Exception as e:
            print(f"Error in DB: {e}")
