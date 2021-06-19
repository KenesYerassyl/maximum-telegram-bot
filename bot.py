import logging 
import messages
import asyncio
import json

from sheets import get_user_info, does_chat_exist, get_user_id, unsubscribe_user, check_user_id, new_sheet_released, get_all_users
from dotenv import load_dotenv
from os import environ, read

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


class GetID(StatesGroup):
    waiting_for_id = State()

async def start(message: types.Message, state: FSMContext):
    await state.finish()
    message_to_send = messages.SEND_ID_MESSAGE
    if message.text != messages.NEW_ID_MESSAGE:
        message_to_send = f"{messages.WELCOME_MESSAGE} {message_to_send}"

    reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard_markup.add(messages.NEW_ID_MESSAGE, messages.CHOOSE_TEST_MESSAGE)

    await ask_for_id(message.chat.id, message_to_send, reply_keyboard_markup)
    await GetID.waiting_for_id.set()

async def close(message: types.Message, state: FSMContext):
    await state.finish()
    if  does_chat_exist(message.chat.id) == -1:
        await message.answer(messages.NOT_SUBSCRIBED)
    else:
        unsubscribe_user(message.chat.id)
        await message.answer(messages.UNSUBSCRIBE_MESSAGE, reply_markup=types.ReplyKeyboardRemove())

async def ask_for_id(chat_id, message_to_send, reply_keyboard_markup=None):
    await bot.send_message(chat_id, message_to_send, reply_markup=reply_keyboard_markup)


async def id_received(message: types.Message, state: FSMContext):
    if check_user_id(message.text, message.chat.id) == False:
        await message.answer(messages.id_failure_code(message.text), parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer(messages.id_succes_code(message.text), parse_mode=ParseMode.MARKDOWN)
        await test_choices(message)
        await state.finish()

async def test_choices(message: types.Message):
    if does_chat_exist(message.chat.id) == -1:
        await ask_for_id(message.chat.id, messages.NEW_ID_MESSAGE)
    else:
        inline_keyboard = InlineKeyboardMarkup()
        with open("sheets.json", "r") as read_file:
            sheets = json.load(read_file).get("sheets")
        for sheet_name in sheets:
            inline_button = InlineKeyboardButton(f'{sheet_name}', callback_data=f'$sheet&chatId$_{sheet_name}_{message.chat.id}')
            inline_keyboard.add(inline_button)
        await message.answer(messages.CHOOSE_TEST_MESSAGE, reply_markup=inline_keyboard)

async def test_name_received(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    user_id = does_chat_exist(int(data[2]))["user_id"]
    if user_id == -1:
        await ask_for_id(data[2], messages.NEW_ID_MESSAGE)
    else:
        result = get_user_info(user_id, data[1])
        if result == None:
            await bot.send_message(int(data[2]), messages.NO_TEST_DATA_FOUND)
        else:
            message_to_send = messages.show_result(data[1]) + get_string_from(result)
            await bot.send_message(int(data[2]), message_to_send)

def register_handlers(dp):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(start, Text(equals=messages.NEW_ID_MESSAGE), state='*')
    dp.register_message_handler(close, commands=['close'], state='*')
    dp.register_message_handler(id_received, state=GetID.waiting_for_id)
    dp.register_message_handler(test_choices, Text(equals=messages.CHOOSE_TEST_MESSAGE))
    dp.register_callback_query_handler(test_name_received, lambda callback_query: callback_query.data.startswith('$sheet&chatId$_'))

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        if new_sheet_released() == True:
            
            with open("sheets.json", "r") as read_file:
                sheets = json.load(read_file)
            sheet_amount = len(sheets["sheets"])
            sheets["sheets"].append(f"Тест {sheet_amount + 1}")

            with open("sheets.json", "w") as write_file:
                json.dump(sheets, write_file)
            
            users = get_all_users()
            for user in users:
                user_info = get_user_info(user["user_id"], f"Тест {sheet_amount + 1}")
                await bot.send_message(user["chat_id"], messages.new_results(f"Тест {sheet_amount + 1}"))
                if user_info == None:
                    await bot.send_message(user["chat_id"], messages.NO_TEST_DATA_FOUND)
                else:
                    message_to_send = messages.show_result(f"Тест {sheet_amount + 1}") + get_string_from(user_info)
                    await bot.send_message(user["chat_id"], message_to_send)

def get_string_from(dict):
    result = ""
    for item in dict.items():
        key, value = item
        if value != 'N/a':
            result += f'{key}: {value}\n'
    return result



if __name__ == '__main__':
    register_handlers(dp)
    asyncio.get_event_loop().create_task(scheduled(15))
    executor.start_polling(dp, skip_updates=True)
