from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.markdown import hcode
from aiogram.dispatcher import FSMContext
from aiogram_calendar import simple_cal_callback, SimpleCalendar

import aiogram_calendar
from datetime import datetime, timedelta

from tgbot.keyboards.reply import *
from tgbot.keyboards.inline import *
from tgbot.misc.states import FSMUser
from tgbot.models.sql_connector import *
from create_bot import bot


async def user_start(message: Message):
    if message.text == 'Назад':
        args = ''
    else:
        args = message.get_args()
    if args == '':
        text = 'Создайте сообщение, выберите время отправки и получателей сообщения'
        kb = main_menu_kb()
    else:
        pass
    await message.delete()
    await FSMUser.home.set()
    await message.answer(text, reply_markup=kb)


async def main_menu(message: Message):
    if message.text == 'Сообщение':
        text = [
            'Подробно объясните где вас искать и что нужно сделать, дайте контакты людей, которые будут с вами\n',
            'Этот текст будет отправлен получателям'
        ]
        kb = back_kb()
        await FSMUser.message.set()
    elif message.text == 'Адресная книга':
        user_id = message.from_user.id
        rec_list = await get_recipients_sql(user_id)
        if len(rec_list) == 0:
            text = ['Адресная книга пуста']
            kb = recipient_kb()
        else:
            pass
    elif message.text == 'Время отправки':
        text = 'Выберите дату отправки'
        kb = date_kb()
    elif message.text == '🎁 Поблагодарить':
        text = [
            'Вы можете поблагодарить создателей бота по ссылке https://yoomoney.ru/fundraise/AMJIwwIzSc4.230219\n',
            'Спасибо! 💔'
        ]
        kb = back_kb()
    else:
        text = ['Недопустимая команда']
        kb = back_kb()
    await message.delete()
    await message.answer('\n'.join(text), reply_markup=kb)


async def get_message(message: Message):
    user_id = message.from_user.id
    new_text = message.text
    text = 'Создайте сообщение, выберите время отправки и получателей сообщения'
    kb = main_menu_kb()
    msg_sql = await get_message_sql(user_id)
    if len(msg_sql) == 0:
        await create_message_sql(user_id, 'message', new_text)
    else:
        await update_message_sql(user_id, 'message', new_text)
    await message.answer(text, reply_markup=kb)


async def add_user(message: Message):
    user_id = message.from_user.id
    link = await get_start_link(user_id, encode=True)
    text = [
        'Для того, чтобы мы могли отправлять сообщения, скиньте получателям ссылку для авторизации в боте',
        f'{hcode(link)}\n',
        'Не будем отправлять ничего, кроме ваших сообщений\n',
        'Оповестим вас, когда они авторизуются'
    ]
    kb = back_kb()
    await message.answer('\n'.join(text), reply_markup=kb)


async def get_date(callback: CallbackQuery, state: FSMContext):
    if callback.data.split(':')[1] == 'today':
        text = 'Выберите время отправки в формате чч:мм'
        kb = back_kb()
        async with state.proxy() as data:
            data['date'] = datetime.today()
    elif callback.data.split(':')[1] == 'tomorrow':
        text = 'Выберите время отправки в формате чч:мм'
        kb = back_kb()
        async with state.proxy() as data:
            data['date'] = datetime.today() + timedelta(days=1)
    else:
        text = 'Выберите дату'
        kb = await aiogram_calendar.SimpleCalendar().start_calendar()
        await callback.message.answer('\n'.join(text), reply_markup=kb)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)



def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(user_start, lambda c: c.text == 'Назад', state='*')
    dp.register_message_handler(main_menu, content_types='text', state=FSMUser.home)
    dp.register_message_handler(get_message, content_types='text', state=FSMUser.message)
    dp.register_message_handler(user_start, lambda c: c.text == 'Назад', state='*')
    dp.register_message_handler(add_user, lambda c: c.text == 'Добавить пользователя', state='*')


