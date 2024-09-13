from aiogram import Router, F
from aiogram.types import Message
from DataStorage import DataStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from Keyboards import main_kb, menu_kb

router = Router()


class InfoState(StatesGroup):
    name = State()


@router.message(F.text == 'Расписание на конкретного человека')
async def chuman(message: Message, state: FSMContext):
    await state.set_state(InfoState.name)
    await message.answer('Введите ФИ', reply_markup=menu_kb())


@router.message(StateFilter(InfoState.name))
async def name(message: Message, state: FSMContext):

    data = await DataStorage.get_alldata(message.text)

    zapisi = []
    for day in data.values():
        for zapis in day:
            if zapis["fi"] == message.text:
                zapisi.append(zapis)

    zapisi.sort(key=lambda x: (sum(map(lambda y: y[0] * y[1], zip(map(int, x["date"].split(".")), [1, 30, 365]))), float(x["time"].replace(":", "."))))

    text = [f"ФИ: {d['fi']}\nТелефон: {d['phone']}\nДата: {d['date']}\nВремя: {d['time']}\nПроцедура: {d['procedure']}\nЦена: {d['price']}"
            for d in zapisi]

    if len(text) == 0:

        await message.answer('На данного человека записей нет! Попробуйте еще раз ввести ФИ')

    else:

        await message.answer("\n\n".join(text), reply_markup=main_kb())

        await state.clear()