from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def date_kb():
    today_button = InlineKeyboardButton(text='Сегодня', callback_data='date:today')
    tomorrow_button = InlineKeyboardButton(text='Завтра', callback_data='date:tomorrow')
    other_button = InlineKeyboardButton(text='Другая дата', callback_data='date:other')
    keyboard = InlineKeyboardMarkup(row_width=1).add(today_button, tomorrow_button, other_button)
    return keyboard
