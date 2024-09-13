from aiogram import Router, F
from DataStorage import DataStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from Keyboards import main_kb, menu_kb

router = Router()


class EditState(StatesGroup):
    choosing_fi_edit = State()
    choosing_par_edit = State()
    choosing_dt_edit = State()
    editing = State()


@router.message(F.text == "Перенести/Отредактировать запись")
async def edit_z(message: Message, state: FSMContext):
    await state.set_state(EditState.choosing_fi_edit)
    await message.answer('Введите ФИ клиента, запись которого Вы бы хотели перенести/редактировать', reply_markup=menu_kb())


@router.message(StateFilter(EditState.choosing_fi_edit))
async def edit_fi(message: Message, state: FSMContext):

    global zapisi
    global f

    f = 1
    data = await DataStorage.get_alldata(message.text)

    zapisi = []
    for day in data.values():
        for zapis in day:
            if zapis["fi"] == message.text:
                zapisi.append(zapis)

    zapisi.sort(key=lambda x: (sum(map(lambda y: y[0] * y[1], zip(map(int, x["date"].split(".")), [1, 30, 365]))), float(x["time"].replace(":", "."))))

    text = [f"ФИ: {d['fi']}\nТелефон: {d['phone']}\nДата: `{d['date']}`\nВремя: `{d['time']}`\nПроцедура: {d['procedure']}\nЦена: {d['price']}"
            for d in zapisi]

    if len(text) == 0:

        await message.answer('На данного человека записей нет, попробуйте еще раз ввести ФИ клиента, запись которого Вы бы хотели перенести/редактировать')

    elif len(text) == 1:

        await message.answer("\n\n".join(text))

        items1 = ["ФИ", "Телефон", "Дата"]
        items2 = ["Время", "Процедура", "Цена"]
        row1 = [KeyboardButton(text=item1) for item1 in items1]
        row2 = [KeyboardButton(text=item2) for item2 in items2]
        await message.answer('Какой параметр Вы бы хотели изменить?', reply_markup=ReplyKeyboardMarkup(
            keyboard=[row1, row2],
            resize_keyboard=True
        ))

        await state.clear()
        await state.set_state(EditState.choosing_par_edit)

    else:

        await message.answer("\n\n".join(text).replace(".", "\."), parse_mode="MarkdownV2")
        await message.answer('Введите дату и время записи, которую Вы бы хотели изменить (например: "01.01.2024 06:09")')

        await state.clear()
        await state.set_state(EditState.choosing_dt_edit)


@router.message(StateFilter(EditState.choosing_dt_edit))
async def edit_dt(message: Message, state: FSMContext):

    global needed_date
    global needed_time
    global f

    t = message.text
    needed_date = t.split()[0]
    needed_time = t.split()[1]
    f = 0

    data = await DataStorage.get_ndnt(needed_date, needed_time)

    if len(data) == 0:

        await message.answer('На данную дату записей нет, попробуйте еще раз ввести дату и время в виде "дд.мм.гггг чч:мм"')

    else:

        text = [
            f"ФИ: {d['fi']}\nТелефон: {d['phone']}\nВремя: {d['time']}\nПроцедура: {d['procedure']}\nЦена: {d['price']}\nДата: {needed_date}"
            for d in data]

        await message.answer("\n\n".join(text))
        items1 = ["ФИ", "Телефон", "Дата"]
        items2 = ["Время", "Процедура", "Цена"]
        row1 = [KeyboardButton(text=item1) for item1 in items1]
        row2 = [KeyboardButton(text=item2) for item2 in items2]
        await message.answer('Какой параметр Вы бы хотели изменить?', reply_markup=ReplyKeyboardMarkup(
            keyboard=[row1, row2],
            resize_keyboard=True
        ))

        await state.clear()
        await state.set_state(EditState.choosing_par_edit)


@router.message(StateFilter(EditState.choosing_par_edit))
async def edit_par(message: Message, state: FSMContext):

    global par

    par = message.text

    if f:

        global needed_date
        global needed_time

        for d in zapisi:
            needed_date = d['date']
            needed_time = d['time']

    await message.answer(f'Введите новое значение параметра "{par}"', reply_markup=menu_kb())

    await state.clear()
    await state.set_state(EditState.editing)


@router.message(StateFilter(EditState.editing))
async def editing(message: Message, state: FSMContext):

    new_par = message.text

    data = await DataStorage.edit_data(needed_date, needed_time, par, new_par)

    if len(data) == 1:
        #
        # items1 = ["Добавить клиента", "Убрать клиента"]
        # items2 = ["Перенести/Отредактировать запись", "Расписание на дату"]
        # items3 = ["Расписание на конкретного человека", "Общее расписание"]
        # row1 = [KeyboardButton(text=item1) for item1 in items1]
        # row2 = [KeyboardButton(text=item2) for item2 in items2]
        # row3 = [KeyboardButton(text=item3) for item3 in items3]

        if par != 'Дата':

            text = [
                f"ФИ: {d['fi']}\nТелефон: {d['phone']}\nВремя: {d['time']}\nПроцедура: {d['procedure']}\nЦена: {d['price']}\nДата: {needed_date}"
                for d in data]

            await message.answer("\n\n".join(text))

        else:

            text = [
                f"ФИ: {d['fi']}\nТелефон: {d['phone']}\nВремя: {d['time']}\nПроцедура: {d['procedure']}\nЦена: {d['price']}\nДата: {new_par}"
                for d in data]

            await message.answer("\n\n".join(text))

        await message.answer('Запись успешно редактирована!', reply_markup=main_kb())

        await state.clear()

    else:

        await message.answer('Запись с указанными данными дата и время не была найдена. Попробуйте еще раз ввести дату и время в формате "дд.мм.гггг чч:мм"', reply_markup=menu_kb())