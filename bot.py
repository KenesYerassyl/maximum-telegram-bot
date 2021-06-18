from aiogram.types.message import ParseMode
from sheets import check_user_id, get_user_info, does_chat_exist, delete_chat
from dotenv import load_dotenv
from os import environ, read

import logging 
import messages
import asyncio
import json

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

    await message.answer(message_to_send, reply_markup=reply_keyboard_markup)
    await GetID.waiting_for_id.set()

async def close(message: types.Message, state: FSMContext):
    if does_chat_exist(message.chat.id) == -1:
        await message.answer(messages.NOT_SUBSCRIBED)
    else:
        delete_chat(message.chat.id)
        await state.finish()
        await message.answer(messages.UNSUBSCRIBE_MESSAGE, reply_markup=types.ReplyKeyboardRemove())

async def id_received(message: types.Message, state: FSMContext):
    if check_user_id(message.text, message.chat.id) == False:
        await message.answer(messages.id_failure_code(message.text), parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer(messages.id_succes_code(message.text), parse_mode=ParseMode.MARKDOWN)
        await test_choices(message)
        await state.finish()

async def test_choices(message: types.Message):
    if does_chat_exist(message.chat.id) == -1:
        await message.answer(messages.NO_USER_ID)
        await start(message=messages.NEW_ID_MESSAGE, state='*')
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
    user_id = does_chat_exist(data[2])
    if user_id == -1:
        await bot.send_message(int(data[2]), messages.NO_USER_ID)
        await start(message=messages.NEW_ID_MESSAGE, state='*')
    else:
        result = get_user_info(user_id, data[1])
        message_to_send = messages.show_result(data[1])
        for item in result.items():
            key, value = item
            message_to_send += f'{key}: {value}\n'
        await bot.send_message(int(data[2]), message_to_send)

def register_handlers(dp):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(start, Text(equals=messages.NEW_ID_MESSAGE), state='*')
    dp.register_message_handler(close, commands=['close'], state='*')
    dp.register_message_handler(id_received, state=GetID.waiting_for_id)
    dp.register_message_handler(test_choices, Text(equals=messages.CHOOSE_TEST_MESSAGE))
    dp.register_callback_query_handler(test_name_received, lambda callback_query: callback_query.data.startswith('$sheet&chatId$_'))

# async def scheduled(wait_for):
#     while True:
#         await asyncio.sleep(wait_for)
#         await bot.send_message(863383312, "HELLO NEGROE YOU GOOD THO?!?!?!")

if __name__ == '__main__':
    register_handlers(dp)
    # asyncio.get_event_loop().create_task(scheduled(5))
    executor.start_polling(dp, skip_updates=True)
