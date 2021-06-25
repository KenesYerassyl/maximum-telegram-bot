NEW_ID_MESSAGE = "ИИН номерді жіберу"
WELCOME_MESSAGE = f"""
Сәлеметсіз бе?!
"MAXIMUM" оқыту орталығының ботына қош келдіңіз☺️
Тест нәтижесін білу үшін төменде көрсетілген ***{NEW_ID_MESSAGE}*** батырмасын басыңыз⤵️\n
"""
SEND_ID_MESSAGE = "ИИН номеріңізді жіберіңіз"
CHOOSE_TEST_MESSAGE = "Тест нәтижесін көрсету"
UNSUBSCRIBE_MESSAGE = "Бот ҝызметін аяқтады, қайта бастау үшін /start командасын жіберіңіз."
NO_USER_ID = "Бот қызметін толық қолдану үшін өз ИИН номеріңізді жазыңыз. ИИН номеріңізді жіберу үшін, ***{NEW_ID_MESSAGE}*** батырмасын басыңыз."
NOT_SUBSCRIBED = "Бот қызметін толық қолдану үшін өз ИИН номеріңізді жазыңыз."

def no_test_data_found(user_id):
    return f"{user_id} ИИН номері бойынша ақпарат табылмады."

def id_succes_code(id):
    return f"""
    💡Сіздің ИИН номеріңіз: ***{id}***. 
    Тест нәтижесін білу үшін өз нұсқаңызды таңдаңыз⬇️
    """

def id_failure_code(id):
    return f"""
ИИН номеріңіз ***{id}*** қате жазылды🚫
Номерді қайта жіберуіңізді сұраймыз.
"""

def new_results(sheet_name):
    return f"Жаңа тест нәтижелері шықты – ***{sheet_name}***."

def get_string_from(dict):
    result = "Құттықтаймыз🥳\n\n📚 Оқу форматы: онлайн/офлайн\n\n"
    result += f"🎓 Оқушының аты-жөні: {list(list(dict.values()))[1]}\n"
    result += f"🏢 Топ: {list(dict.values())[2]}\n"
    result += f"📄 Нұсқа: {list(dict.values())[3]}\n"
    result += f"🗓️ Күні: {list(dict.values())[4]}\n"
    result += f"📊 Жалпы балл: {list(dict.values())[5]}\n\n"
    result += "Тест нәтижесі:\n"
    result += f"✅ Оқу сауаттылығы: {list(dict.values())[6]}/20\n"
    result += f"✅ Қазақстан тарихы: {list(dict.values())[7]}/15\n"
    result += f"✅ Математикалық сауаттылық: {list(dict.values())[8]}/15\n"
    index = 9
    while index < len(dict.items()):
        key, value = list(dict.items())[index]
        if value != 'N/a':
            result += f'✅{key}: {value}/45\n'
        index += 1
    return result