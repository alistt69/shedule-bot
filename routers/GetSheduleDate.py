from aiogram import Router, F
from DataStorage import DataStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message
from Keyboards import main_kb, menu_kb

router = Router()


class InfoState(StatesGroup):
    day = State()


@router.message(F.text == "Расписание на дату")
async def schedule(message: Message, state: FSMContext):
    await state.set_state(InfoState.day)
    await message.answer("Введите дату в формате дд.мм.гггг, на которую хотели бы посмотреть расписание", reply_markup=menu_kb())


@router.message(StateFilter(InfoState.day))
async def day(message: Message, state: FSMContext):

    data = await DataStorage.get_data(message.text)

    text = [f"ФИ: {d['fi']}\nТелефон: {d['phone']}\nВремя: {d['time']}\nПроцедура: {d['procedure']}\nЦена: {d['price']}" for d in data]

    if len(text) == 0:

        await message.answer('На данную дату записей нет', reply_markup=main_kb())

    else:

        await message.answer("\n\n".join(text), reply_markup=main_kb())

    await state.clear()
