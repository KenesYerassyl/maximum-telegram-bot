import logging 
import messages
import asyncio

from sheets_testresults import get_user_info, does_chat_exist, get_user_id, unsubscribe_user, check_user_id, new_sheet_released, get_all_users, get_all_tests
from dotenv import load_dotenv
from os import environ, read
from attendance_fsm import AttendanceFSM

from aiogram.types.message import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

logging .basicConfig(level=logging.INFO)

bot = Bot(token=environ.get("BOT_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

attendance_fsm = AttendanceFSM(bot, dp)

class GetID(StatesGroup):
    waiting_for_id = State()

# NOTE: start command
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    message_to_send = f"{messages.WELCOME_MESSAGE}"
    reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    reply_keyboard_markup.add(messages.NEW_ID_MESSAGE, messages.CHOOSE_TEST_MESSAGE, messages.SCHEDULE_MESSAGE, messages.ATTENDANCE_MESSAGE)

    await message.answer(message_to_send, reply_markup=reply_keyboard_markup, parse_mode=ParseMode.MARKDOWN)

# NOTE: asks for ID, sets state from general to 'waiting_for_id'
async def ask_for_id(message: types.Message):
    await message.answer(messages.SEND_ID_MESSAGE, parse_mode=ParseMode.MARKDOWN)
    await GetID.waiting_for_id.set()

# NOTE: observes for any message in 'wating_for_id' state, after successfull ID finishes the state
async def id_received(message: types.Message, state: FSMContext):
    if check_user_id(message.text, message.chat.id) == False:
        await message.answer(messages.id_failure_code(message.text), parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer(messages.id_succes_code(message.text), parse_mode=ParseMode.MARKDOWN)
        await test_choices(message)
        await state.finish()

# NOTE: sends the multiple buttons with test numbers on them
async def test_choices(message: types.Message):
    if does_chat_exist(message.chat.id) == -1:
        await bot.send_message(message.chat.id, messages.NO_USER_ID_MESSAGE, parse_mode=ParseMode.MARKDOWN)
    else:
        inline_keyboard = InlineKeyboardMarkup()
        sheets = get_all_tests()
        for sheet_name in sheets:
            inline_button = InlineKeyboardButton(f'{sheet_name["test_name"]}', callback_data=f'$sheet&chatId$_{sheet_name["test_name"]}_{message.chat.id}')
            inline_keyboard.add(inline_button)
        await message.answer(messages.CHOOSE_TEST_MESSAGE, reply_markup=inline_keyboard)

# NOTE: callback query handler which fires when one of the test results is chosen
async def test_name_received(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    user_id = does_chat_exist(int(data[2]))
    if user_id == -1:
        await bot.send_message(int(data[2]), messages.NO_USER_ID_MESSAGE, parse_mode=ParseMode.MARKDOWN)
    else:
        print(user_id)
        print(data[1])
        result = get_user_info(user_id, data[1])
        if result == None:
            await bot.send_message(int(data[2]), messages.no_test_data_found(user_id), parse_mode=ParseMode.MARKDOWN)
        else:
            message_to_send = messages.get_string_from(result)
            await bot.send_message(int(data[2]), message_to_send)

# NOTE: simply sends the schedule
async def send_schedule(message: types.Message):
    await message.answer(environ.get("SCHEDULE_LINK"))

# NOTE: close command
async def close(message: types.Message, state: FSMContext):
    await state.finish()
    if  does_chat_exist(message.chat.id) == -1:
        await message.answer(messages.NOT_SUBSCRIBED_MESSAGE)
    else:
        unsubscribe_user(message.chat.id)
        await message.answer(messages.UNSUBSCRIBE_MESSAGE, reply_markup=types.ReplyKeyboardRemove())

def register_handlers(dp):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(ask_for_id, Text(equals=messages.NEW_ID_MESSAGE))
    dp.register_message_handler(close, commands=['close'], state='*')
    dp.register_message_handler(id_received, state=GetID.waiting_for_id)
    dp.register_message_handler(test_choices, Text(equals=messages.CHOOSE_TEST_MESSAGE))
    dp.register_message_handler(send_schedule, Text(equals=messages.SCHEDULE_MESSAGE))
    dp.register_callback_query_handler(test_name_received, lambda callback_query: callback_query.data.startswith('$sheet&chatId$_'))

async def scheduled_testresults(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        new_sheet = new_sheet_released()
        if new_sheet != None:
            users = get_all_users()
            for user in users:
                user_info = get_user_info(user["user_id"], new_sheet)
                if user_info != None:
                    await bot.send_message(user["chat_id"], messages.new_results(new_sheet), parse_mode=ParseMode.MARKDOWN)
                    await bot.send_message(user["chat_id"], messages.get_string_from(user_info))

async def scheduled_attendance(wait_for):
    pass

async def make_notification(message):
    users = get_all_users()
    reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    reply_keyboard_markup.add(messages.NEW_ID_MESSAGE, messages.CHOOSE_TEST_MESSAGE, messages.SCHEDULE_MESSAGE, messages.ATTENDANCE_MESSAGE)
    for user in users:
        await bot.send_message(user["chat_id"], message, reply_markup=reply_keyboard_markup)

if __name__ == '__main__':
    register_handlers(dp)
    asyncio.get_event_loop().create_task(scheduled_testresults(28 * 60))
    executor.start_polling(dp, skip_updates=True)
    
    
