import datetime
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove
from pyasn1.type.base import Asn1ItemBase
from sheets import check_user_id, get_user_scores
from dotenv import load_dotenv
from os import environ

import logging 
import messages
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

load_dotenv()

logging .basicConfig(level=logging.INFO)

bot = Bot(token=environ.get("BOT_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class GetID(StatesGroup):
    waiting_for_id = State()

async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(messages.WELCOME_MESSAGE, reply_markup=ReplyKeyboardRemove())
    await GetID.waiting_for_id.set()

async def id_received(message: types.Message, state: FSMContext):
    does_exist = check_user_id(message.text, message.chat.id)
    if does_exist == False:
        await message.answer(messages.id_failure_code(message.text))
    else:
        scores = get_user_scores(message.text)
        await message.answer(
f"""{messages.id_succes_code(message.text)} 
Kazakh Language: {scores[0]}
History: {scores[1]}
Computer Science: {scores[2]}
Math: {scores[3]}
Physics: {scores[4]}""")
        await state.finish()

def register_handlers(dp):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(id_received, state=GetID.waiting_for_id)

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        now = datetime.utcnow()
        await bot.send_message("Nigga you good tho!")

async def main():
    register_handlers(dp)
    await asyncio.get_event_loop().create_task(scheduled(5))
    executor.start_polling(dp, skip_updates=True)