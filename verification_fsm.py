import messages

from sheets_testresults import check_user_id

from aiogram.types.message import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

class GetID(StatesGroup):
    waiting_for_id = State()

class VerificationFSM:

    def __init__(self, bot, dp: Dispatcher) -> None:
        self.bot = bot
        dp.register_message_handler(self.verification_message, Text(equals=messages.NEW_ID_MESSAGE))
        dp.register_message_handler(self.verification_received, state=GetID.waiting_for_id)
    
    async def verification_message(self, message: types.Message):

        reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        reply_keyboard_markup.add(messages.BACK_MESSAGE)

        await message.answer(messages.SEND_ID_MESSAGE, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_keyboard_markup)
        await GetID.waiting_for_id.set()


    async def verification_received(self, message: types.Message, state: FSMContext):
        if check_user_id(message.text, message.chat.id) == False:
            await message.answer(messages.id_failure_code(message.text), parse_mode=ParseMode.MARKDOWN)
        else:

            reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            reply_keyboard_markup.add(*messages.MAIN_KEYBOARD_SET)

            await message.answer(messages.id_succes_code(message.text), parse_mode=ParseMode.MARKDOWN, reply_markup=reply_keyboard_markup)
            await state.finish()