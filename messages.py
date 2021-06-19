WELCOME_MESSAGE = "Hello there!"
SEND_ID_MESSAGE = "Please send me the student's ID."
NEW_ID_MESSAGE = "Send me your ID"
CHOOSE_TEST_MESSAGE = "Choose the test"
UNSUBSCRIBE_MESSAGE = "You have unsubscribed successfully. Bot will not send you messages anymore."
NO_USER_ID = "Sorry, please send me your ID first."
NOT_SUBSCRIBED = "You have not subscribed yet."
NO_TEST_DATA_FOUND = "I could not find any information about you in this test."

def show_result(sheet_name):
    return f"Your results in {sheet_name}:\n"

def id_succes_code(id):
    return f"Your ID: ***{id}*** found successfully. Choose the test:"

def id_failure_code(id):
    return f"Sorry, user with such ID: ***{id}*** does not exist, please try again!"

def new_results(sheet_name):
    return f"Results of test {sheet_name} are released!"