from aiogram import Router, F
from aiogram.types import Message
from DataStorage import DataStorage

router = Router()


@router.message(F.text == 'Общее расписание')
async def allshedule(message: Message):
    data = await DataStorage.get_alldata(message.text)
    zapisi = []
    for day in data.values():
        zapisi += day

    zapisi.sort(key=lambda x: (sum(map(lambda y: y[0] * y[1], zip(map(int, x["date"].split(".")), [1, 30, 365]))), float(x["time"].replace(":", "."))))

    t = [f"ФИ: {d['fi']}\nТелефон: {d['phone']}\nДата: {d['date']}\nВремя: {d['time']}\nПроцедура: {d['procedure']}\nЦена: {d['price']}"
        for d in zapisi]

    r = 10
    os = len(t) % r
    for i in range(0, len(t) - os, r):
        text = []
        for _ in range(r):
            text.append(t[i + _])
        await message.answer("\n\n".join(text))
    if os:
        await message.answer("\n\n".join(t[-os:]))