from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb():
    message_button = KeyboardButton('Сообщение')
    recipients_button = KeyboardButton('Адресная книга')
    dtime_button = KeyboardButton('Время отправки')
    donate_button = KeyboardButton('🎁 Поблагодарить')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.row(message_button).row(recipients_button).row(dtime_button).row(donate_button)
    return keyboard


def back_kb():
    back_button = KeyboardButton('Назад')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.row(back_button)
    return keyboard


def recipient_kb():
    add_button = KeyboardButton('Добавить пользователя')
    back_button = KeyboardButton('Назад')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.row(add_button).row(back_button)
    return keyboard
