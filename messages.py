WELCOME_MESSAGE = "Hello there! Please send me the student's ID."
KAZ_LANG = "Kazakh Language"
HISTORY = "History"
COMPUTER_SCI =  "Computer Science"
PHYSICS = "Physics"
MATH = "Math"

def id_succes_code(id):
    return f"Your ID: {id} found successfully. Choose the subject:"

def id_failure_code(id):
    return f"Sorry, user with such ID: {id} does not exist, please try again!"
