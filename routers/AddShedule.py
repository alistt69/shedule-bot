from aiogram import Router, F
from DataStorage import DataStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message
from Keyboards import main_kb, menu_kb

router = Router()


class States(StatesGroup):
    choosing_fi_add = State()
    choosing_phone = State()
    choosing_date = State()
    choosing_time = State()
    choosing_procedure = State()
    choosing_price = State()


@router.message(F.text == "Добавить клиента")
async def add_client(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(States.choosing_fi_add)
    await message.answer("Введите ФИ клиента", reply_markup=menu_kb())


@router.message(StateFilter(States.choosing_fi_add))
async def choosing_fi(message: Message, state: FSMContext):
    await state.update_data(fi=message.text)
    await message.answer("Хорошо! Теперь введите номер телефона")
    await state.set_state(States.choosing_phone)


@router.message(StateFilter(States.choosing_phone))
async def choosing_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Хорошо! Теперь введите дату (дд.мм.гггг)")
    await state.set_state(States.choosing_date)


@router.message(StateFilter(States.choosing_date))
async def choosing_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Хорошо! Теперь введите время (чч:мм)")
    await state.set_state(States.choosing_time)


@router.message(StateFilter(States.choosing_time))
async def choosing_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("Хорошо! Теперь введите процедуру")
    await state.set_state(States.choosing_procedure)


@router.message(StateFilter(States.choosing_procedure))
async def choosing_procedure(message: Message, state: FSMContext):
    await state.update_data(procedure=message.text)
    await message.answer("Хорошо! Теперь введите цену")
    await state.set_state(States.choosing_price)


@router.message(StateFilter(States.choosing_price))
async def choosing_price(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    await message.answer("Хорошо! Информация сохранена", reply_markup=main_kb())
    data = await state.get_data()
    await DataStorage.add_data(data["date"], data)
    await state.clear()