import logging
import asyncio
from routers import *
from Keyboards import main_kb, menu_kb
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from os import environ
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
from datetime import datetime


from DataStorage import DataStorage
from JSONStorage import Storage

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=environ.get("BOT_TOKEN"))
dp = Dispatcher(storage=Storage())


@dp.message(F.text == 'Вернуться на главный экран')
async def menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Процесс был приостановлен, вы вернулись на главное меню!', reply_markup=main_kb())

@dp.message(CommandStart())
async def start(message: Message):
    # items1 = ["Добавить клиента", "Убрать клиента"]
    # items2 = ["Перенести/Отредактировать запись", "Расписание на дату"]
    # items3 = ["Расписание на конкретного человека", "Общее расписание"]
    # row1 = [KeyboardButton(text=item1) for item1 in items1]
    # row2 = [KeyboardButton(text=item2) for item2 in items2]
    # row3 = [KeyboardButton(text=item3) for item3 in items3]
    await message.answer("Привет! Я умею добавлять клиентов, убирать записи, переносить их, редактировать и напоминать о них. Могу показывать общее расписание и на конкретного человека/дату. По всем вопросам советую писать @alistt69", reply_markup=main_kb())


async def main():
    dp.include_routers(AddSheduleRouter, DelSheduleRouter, EditSheduleRouter, GetAllSheduleRouter, GetSheduleDateRouter, GetShedulePersonRouter)
    await dp.start_polling(bot, skip_updates=True)

