import asyncio
from datetime import datetime, timedelta

from DataStorage import DataStorage
from bot import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
async def periodic_task():
    date = datetime.now() + timedelta(days=1)

    data = await DataStorage.get_data(date.strftime("%d.%m.%Y"))

    print(date.strftime("%d.%m.%Y"))

    text = [
        f"ФИ: {d['fi']}\nТелефон: {d['phone']}\nВремя: {d['time']}\nПроцедура: {d['procedure']}\nЦена: {d['price']}"
        for d in data]

    if len(text) != 0:
        await bot.send_message(1690641228, 'На завтра у Вас запланирована запись!')
        await bot.send_message(1690641228, "\n\n".join(text))

async def run_task():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(periodic_task, trigger="cron", hour="19", minute="00")

    scheduler.start()
