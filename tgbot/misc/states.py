from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    home = State()
    message = State()
    recipients = State()
    dtime = State()



