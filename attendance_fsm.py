import messages

from sheets_attendance import check_attendance
from sheets_testresults import does_chat_exist
from datetime import date

from aiogram.types.message import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

class GetDate(StatesGroup):
    waiting_for_date = State()

class AttendanceFSM:

    def __init__(self, bot, dp: Dispatcher) -> None:
        self.bot = bot
        dp.register_message_handler(self.attendance_message, Text(equals=messages.ATTENDANCE_MESSAGE))
        dp.register_callback_query_handler(self.attendance_date_received, lambda callback_query: callback_query.data.startswith('$name&chatId$_'))
        dp.register_message_handler(self.date_received, state=GetDate.waiting_for_date)

    async def attendance_message(self, message: types.Message):
        if does_chat_exist(message.chat.id) == -1:
            await self.bot.send_message(message.chat.id, messages.NO_USER_ID_MESSAGE, parse_mode=ParseMode.MARKDOWN)
        else:
            inline_keyboard = InlineKeyboardMarkup()
            inline_keyboard.row(
                InlineKeyboardButton(messages.TODAY_MESSAGE, callback_data=f'$name&chatId$_{messages.TODAY_MESSAGE}_{message.chat.id}'),
                InlineKeyboardButton(messages.OTHER_DATE_MESSAGE, callback_data=f'$name&chatId$_{messages.OTHER_DATE_MESSAGE}_{message.chat.id}')
            )
            await message.answer(messages.SPECIFY_ATTENDANCE_DATE_MESSAGE, reply_markup=inline_keyboard)
 
    async def attendance_date_received(self, callback_query: types.CallbackQuery):
        data = callback_query.data.split('_')
        user_id = does_chat_exist(int(data[2]))
        if user_id == -1:
            await self.bot.send_message(int(data[2]), messages.NO_USER_ID_MESSAGE, parse_mode=ParseMode.MARKDOWN)
        else:
            if data[1] == messages.TODAY_MESSAGE:
                today = date.today().strftime("%d/%m/%Y")
                date_list = today.split('/')
                attendance_result = check_attendance(user_id, date_list[1], str(messages.convert_to_int(date_list[0])))
                if attendance_result == None:
                    await self.bot.send_message(int(data[2]), messages.no_test_data_found(user_id), parse_mode=ParseMode.MARKDOWN)
                else:
                    (attendance_status, full_name) = attendance_result
                    await self.bot.send_message(int(data[2]), messages.attendance_result(attendance_status, date_list[0], date_list[1], full_name))
            elif data[1] == messages.OTHER_DATE_MESSAGE:
                await self.bot.send_message(int(data[2]), messages.DATE_SPECS_MESSAGE, parse_mode=ParseMode.MARKDOWN)
                await GetDate.waiting_for_date.set()

    async def date_received(self, message: types.Message, state: FSMContext):
        user_id = does_chat_exist(message.chat.id)
        if user_id == -1:
            await message.answer(messages.NO_USER_ID_MESSAGE, parse_mode=ParseMode.MARKDOWN)
        else:
            if len(message.text) != 5:
                await message.answer(messages.date_failure_code(message.text), parse_mode=ParseMode.MARKDOWN)
                return 

            if not ('0' <= message.text[0] <= '9' and '0' <= message.text[1] <= '9' and '0' <= message.text[3] <= '9' and '0' <= message.text[4] <= '9' and message.text[2] == '/'):
                await message.answer(messages.date_failure_code(message.text), parse_mode=ParseMode.MARKDOWN)
                return 

            day_int = messages.convert_to_int(f"{message.text[0]}{message.text[1]}")
            month_int = messages.convert_to_int(f"{message.text[3]}{message.text[4]}")
            day_str = f"{message.text[0]}{message.text[1]}"
            month_str = f"{message.text[3]}{message.text[4]}"

            if not (1 <= day_int <= 31 and 1 <= month_int <= 12):
                await message.answer(messages.date_failure_code(message.text), parse_mode=ParseMode.MARKDOWN)
                return 

            attendance_result = check_attendance(user_id, month_str, str(day_int))

            if attendance_result == None:
                await message.answer(messages.no_test_data_found(user_id), parse_mode=ParseMode.MARKDOWN)
                await state.finish()
            else:
                (attendance_status, full_name) = attendance_result
                await message.answer(messages.attendance_result(attendance_status, day_str, month_str, full_name))
                await state.finish()


    