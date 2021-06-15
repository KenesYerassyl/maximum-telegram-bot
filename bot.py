from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove
from pyasn1.type.base import Asn1ItemBase
from sheets import check_user_id, get_user_scores

import config
import logging 
import messages

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

logging .basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
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

if __name__ == '__main__':
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)