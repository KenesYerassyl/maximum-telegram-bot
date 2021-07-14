from sheets_attendance import check_attendance
from aiogram.types.base import Boolean

# attendance fsm messages
ATTENDANCE_MESSAGE = "Посещяемость"
SPECIFY_ATTENDANCE_DATE_MESSAGE = "Қай күнді көргіңіз келеді"
TODAY_MESSAGE = "Бүгін"
OTHER_DATE_MESSAGE = "Басқа күн"
DATE_SPECS_MESSAGE = "Білгіңіз келген күнді ***кк/аа*** түрінде жазып жіберіңіз. Мысалы 01/06 деген 1-ші Маусым дегенді білдіреді."

MONTH_RU = {
    "01" : "Январь",
    "02" : "Февраль",
    "03" : "Март",
    "04" : "Апрель",
    "05" : "Май",
    "06" : "Июнь",
    "07" : "Июль",
    "08" : "Август",
    "09" : "Сентябрь",
    "10" : "Октябрь",
    "11" : "Ноябрь",
    "12" : "Декабрь"
}

MONTH_KZ = {
    "01" : "Қаңтар",
    "02" : "Ақпан",
    "03" : "Наурыз",
    "04" : "Сәуір",
    "05" : "Мамыр",
    "06" : "Маусым",
    "07" : "Шілде",
    "08" : "Тамыз",
    "09" : "Қыркүйек",
    "10" : "Қазан",
    "11" : "Қараша",
    "12" : "Желтоқсан"
}

# review fsm messages
REVIEW_MESSAGE = "Кері байланыс беру"
REVIEW_CONTENT_MESSAGE = "Кері байланыс қалдырғыңыз келгені үшін рахмет!\n\nСіз маған кері байланыстың мазмұнын жібергеннен кейін, сізде оны тексеруге және жіберуден бастартуға мүмкіндік болады.\n\nМаған кері байланыстың мәтінін жіберіңіз."
REVIEWER_NAME_MESSAGE = "Керемет! Енді кері байланыс берушінің атын жөнін жіберіңіз."
REVIEW_ASSESSMENT_MESSAGE = "Өте жақсы! Біздің мекеменің жұмысына қаншалықты көңіліңіз толады? Төменде шыққан арнайы смайликтер арқылы жауап беріңіз."
REVIEW_ASSESSMENT_KEYBOARD_SET = ['😡', '🙁', '😐', '😇', '😁']
REVIEW_ASSESSMENT_FAILURE_MESSAGE = "Өтініш, баға беру үшін астында шыққан смайликтерді пайдаланыңыз."
REVIEW_CONFIRMATION_MESSAGE = "Осы күйде жібергіңіз келеді ме?"
REVIEW_ACCEPT_MESSAGE = "Иә"
REVIEW_CANCEL_MESSAGE = "Жоқ"
REVIEW_CONFIRMATION_FAILURE_MESSAGE = "Өтініш, астында шыққан батырмалар арқылы жауап беріңіз."
REVIEW_CANCELLATION_MESSAGE = f"Сіздің кері байланысыңыз жойылды. Егер басынан жібергіңіз келсе ***{REVIEW_MESSAGE}*** батырмасын басыңыз."
REVIEW_FINISHING_MESSAGE = "Сіздің кері байланысыңыз жіберілді🥳👏!"
REVIEW_FOR_CLIENT_MESSAGE = "Кері байланыс қабылданды."

# main messages
NEW_ID_MESSAGE = "ИИН номерді жіберу"
WELCOME_MESSAGE = f"""
Сәлеметсіз бе?!
"MAXIMUM" оқыту орталығының ботына қош келдіңіз☺️
Тест нәтижесін білу үшін төменде көрсетілген ***{NEW_ID_MESSAGE}*** батырмасын басыңыз⤵️\n
"""
SEND_ID_MESSAGE = "ИИН номеріңізді жіберіңіз"
CHOOSE_TEST_MESSAGE = "Тест нәтижесін көрсету"
UNSUBSCRIBE_MESSAGE = "Бот ҝызметін аяқтады, қайта бастау үшін /start командасын жіберіңіз."
NO_USER_ID_MESSAGE = f"Бот қызметін толық қолдану үшін өз ИИН номеріңізді жазыңыз. ИИН номеріңізді жіберу үшін, ***{NEW_ID_MESSAGE}*** батырмасын басыңыз."
NOT_SUBSCRIBED_MESSAGE = "Бот қызметін толық қолдану үшін өз ИИН номеріңізді жазыңыз."
SCHEDULE_MESSAGE = "Сабақ кестесін көру"
MAIN_KEYBOARD_SET = [NEW_ID_MESSAGE, CHOOSE_TEST_MESSAGE, SCHEDULE_MESSAGE, ATTENDANCE_MESSAGE, REVIEW_MESSAGE]
BOT_FAILURE_MESSAGE = "Бот жұмысында қате кетті. Басынан тырысып көріңіз!"

# main message functions
def no_test_data_found(user_id):
    return f"***{user_id}*** ИИН номері бойынша ақпарат табылмады."

def id_succes_code(id):
    return f"💡Сіздің ИИН номеріңіз: ***{id}***.\nТест нәтижесін білу үшін өз нұсқаңызды таңдаңыз⬇️"

def id_failure_code(id):
    return f"ИИН номеріңіз ***{id}*** қате жазылды🚫\nНомерді қайта жіберуіңізді сұраймыз."

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
            result += f'✅ {key}: {value}/45\n'
        index += 1
    return result


# attendance fsm message functions
def convert_to_int(day):
        return int(day[1]) if day[0] == '0' else int(day)

def get_suffix(day):
    if day[1] == '6' or day[1] == '9' or day[1] == '0':
        return 'шы'
    else:
        return 'ші'

def attendance_result(check, day, month, full_name):
    attendance = f"{check} минутқа кешігіп келді"
    if check == '+':
        attendance = "қатысты"
    elif check == '-':
        attendance = "қатыспады"
    elif check == '=':
        return f"{convert_to_int(day)}-{get_suffix(day)} {MONTH_KZ[month]} күні {full_name} сабақтан сұранып кетті."    
    return f"{convert_to_int(day)}-{get_suffix(day)} {MONTH_KZ[month]} күні {full_name} сабаққа {attendance}."

def date_failure_code(date):
    return f"Жіберілген күннің форматы қате ***{date}*** 🚫\nКүн және айды қайта жіберуіңізді сұраймыз."

# review message functions

def construct_review(name, review, assessment):
    return f"***Аты-жөні:*** {name}\n***Кері байланыс:*** {review}\n***Берілген баға:*** {assessment}"
    