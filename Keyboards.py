from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup


def main_kb() -> ReplyKeyboardMarkup:
    items1 = ["Добавить клиента", "Убрать клиента"]
    items2 = ["Перенести/Отредактировать запись", "Расписание на дату"]
    items3 = ["Расписание на конкретного человека", "Общее расписание"]
    row1 = [KeyboardButton(text=item1) for item1 in items1]
    row2 = [KeyboardButton(text=item2) for item2 in items2]
    row3 = [KeyboardButton(text=item3) for item3 in items3]

    keyboard = ReplyKeyboardMarkup(
        keyboard=[row1, row2, row3],
        resize_keyboard=True
    )

    return keyboard


def menu_kb() -> ReplyKeyboardMarkup:
    items1 = ["Вернуться на главный экран"]
    row1 = [KeyboardButton(text=item1) for item1 in items1]

    keyboard = ReplyKeyboardMarkup(
        keyboard=[row1],
        resize_keyboard=True
    )

    return keyboard

