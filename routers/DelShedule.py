from aiogram import Router, F
from DataStorage import DataStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message
from Keyboards import main_kb, menu_kb

from utils import gen_message

router = Router()


class DelState(StatesGroup):
    choosing_fi_del = State()
    choosing_dt = State()


@router.message(F.text == "Убрать клиента")
async def del_client(message: Message, state: FSMContext):
    await state.set_state(DelState.choosing_fi_del)
    await message.answer("Введите ФИ клиента, запись которого Вы хотите убрать", reply_markup=menu_kb())


@router.message(StateFilter(DelState.choosing_fi_del))
async def del_fi(message: Message, state: FSMContext):
    data = await DataStorage.get_alldata(message.text)

    zapisi = []

    for day in data.values():
        for zapis in day:
            if zapis["fi"] == message.text:
                zapisi.append(zapis)

    if len(zapisi) == 0:

        await message.answer('Такого клиента не существует! Попробуйте еще раз написать ФИ!')

    elif len(zapisi) == 1:

        for d in zapisi:
            needed_date = d['date']
            needed_time = d['time']

        data = await DataStorage.replace_data(needed_date, needed_time)
        text = [gen_message(d, date=needed_date) for d in data]

        await message.answer("\n\n".join(text))
        await message.answer('Запись успешно отменена!', reply_markup=main_kb())

        await state.clear()

    else:

        text = [gen_message(d, ["date", "time"]) for d in zapisi]
        await message.answer("\n\n".join(text).replace(".", "\."), parse_mode="MarkdownV2")
        await message.answer('Введите дату и время записи, которую Вы бы хотели удалить (например: "01.01.2024 06:09")')

        await state.clear()
        await state.set_state(DelState.choosing_dt)


@router.message(StateFilter(DelState.choosing_dt))
async def del_dt(message: Message, state: FSMContext):
    t = message.text
    needed_date = t.split()[0]
    needed_time = t.split()[1]

    data = await DataStorage.replace_data(needed_date, needed_time)

    if len(data) == 0:

        await message.answer(
            'На данные дату и время не было найдено записей, попробуйте ввести дату и время еще раз в формате дд.мм.гггг чч:мм')

    else:

        text = [
            gen_message(d, date=needed_date) for d in data]

        await message.answer("\n\n".join(text))
        await message.answer('Запись успешно отменена!', reply_markup=main_kb())

        await state.clear()
