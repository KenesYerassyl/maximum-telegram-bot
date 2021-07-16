import messages

from dotenv import load_dotenv
from os import environ

from aiogram.types.message import Message, ParseMode
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

class GetReview(StatesGroup):
    waiting_for_review = State()
    waiting_for_name = State()
    waiting_for_assessment = State()
    waiting_for_confirmation = State()

class ReviewFSM:

    def __init__(self, bot, dp: Dispatcher) -> None:
        self.bot = bot
        dp.register_message_handler(self.review_message, Text(equals=messages.REVIEW_MESSAGE))
        dp.register_message_handler(self.review_received, state=GetReview.waiting_for_review)
        dp.register_message_handler(self.name_received, state=GetReview.waiting_for_name)
        dp.register_message_handler(self.assessment_received, state=GetReview.waiting_for_assessment)
        dp.register_message_handler(self.confirmation_received, state=GetReview.waiting_for_confirmation)


    async def review_message(self, message: types.Message):
        await message.answer(messages.REVIEW_CONTENT_MESSAGE, reply_markup=types.ReplyKeyboardRemove())
        await GetReview.waiting_for_review.set()

    async def review_received(self, message: types.Message, state: FSMContext):
        await state.update_data(review=message.text)
        await message.answer(messages.REVIEWER_NAME_MESSAGE)
        await GetReview.waiting_for_name.set()

    async def name_received(self, message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        
        reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
        reply_keyboard_markup.add(*messages.REVIEW_ASSESSMENT_KEYBOARD_SET)

        await message.answer(messages.REVIEW_ASSESSMENT_MESSAGE, reply_markup=reply_keyboard_markup)
        await GetReview.waiting_for_assessment.set()

    async def assessment_received(self, message: types.Message, state: FSMContext):
        if message.text not in messages.REVIEW_ASSESSMENT_KEYBOARD_SET:
            await message.answer(messages.REVIEW_ASSESSMENT_FAILURE_MESSAGE)
        else:
            await state.update_data(assessment=message.text)
            user_data = await state.get_data()
            review = user_data.get('review')
            name = user_data.get('name')
            assessment = user_data.get('assessment')
            if review != None and name != None and assessment != None:

                reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
                reply_keyboard_markup.add(messages.REVIEW_ACCEPT_MESSAGE, messages.REVIEW_CANCEL_MESSAGE)

                await message.answer(f"{messages.construct_review(name, review, assessment)}\n\n{messages.REVIEW_CONFIRMATION_MESSAGE}", reply_markup=reply_keyboard_markup, parse_mode=ParseMode.MARKDOWN)
                await GetReview.waiting_for_confirmation.set()
            else:
                reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                reply_keyboard_markup.add(*messages.MAIN_KEYBOARD_SET)

                await message.answer(messages.BOT_FAILURE_MESSAGE, reply_markup=reply_keyboard_markup)
                await state.finish()


    async def confirmation_received(self, message: types.Message, state: FSMContext):
        if message.text != messages.REVIEW_ACCEPT_MESSAGE and message.text != messages.REVIEW_CANCEL_MESSAGE:
            await message.answer(messages.REVIEW_CONFIRMATION_FAILURE_MESSAGE)
        else:

            reply_keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            reply_keyboard_markup.add(*messages.MAIN_KEYBOARD_SET)
            
            if message.text == messages.REVIEW_CANCEL_MESSAGE:
                await message.answer(messages.REVIEW_CANCELLATION_MESSAGE, reply_markup=reply_keyboard_markup, parse_mode=ParseMode.MARKDOWN)
            else:
                user_data = await state.get_data()
                review = user_data.get('review')
                name = user_data.get('name')
                assessment = user_data.get('assessment')
                if review != None and name != None and assessment != None:
                    await self.bot.send_message(int(environ.get("CLIENT_CHAT_ID")), f"{messages.REVIEW_FOR_CLIENT_MESSAGE}\n\n{messages.construct_review(name, review, assessment)}", parse_mode=ParseMode.MARKDOWN)
                    await message.answer(messages.REVIEW_FINISHING_MESSAGE, reply_markup=reply_keyboard_markup)
                else:
                    await message.answer(messages.BOT_FAILURE_MESSAGE, reply_markup=reply_keyboard_markup)
            await state.finish()